#!/usr/bin/env python3
"""Validate paired routing outputs, documented counts and manual policy.

Run: python3 .github/scripts/validate-rules.py [--baseline COMMIT] [--report FILE]
Requires PyYAML. This verifier never fetches sources or mutates rule files.
"""
from __future__ import annotations
import argparse, collections, ipaddress, json, pathlib, re, subprocess
import yaml
from typing import Any
ROOT=pathlib.Path(__file__).resolve().parents[2]
EXPECTED={'AI','AWS','Ads','Apple','AppleCN','China','Crypto','Douyin','Game','GitHub','Google','LAN','Pay','Proxy','Speedtest','Streaming','Telegram'}
TYPES={'DOMAIN','DOMAIN-SUFFIX','DOMAIN-KEYWORD','DOMAIN-WILDCARD','IP-CIDR','IP-CIDR6','IP-ASN','PROCESS-NAME'}
GEMINI={
 'DOMAIN,ai.google.dev','DOMAIN,aida.googleapis.com','DOMAIN,aisandbox-pa.googleapis.com',
 'DOMAIN,alkalicore-pa.clients6.google.com','DOMAIN,alkalimakersuite-pa.clients6.google.com',
 'DOMAIN,daily-cloudcode-pa.googleapis.com','DOMAIN,generativelanguage.googleapis.com',
 'DOMAIN,makersuite.google.com','DOMAIN,robinfrontend-pa.googleapis.com',
 'DOMAIN-SUFFIX,ai.google.dev','DOMAIN-SUFFIX,aistudio.google.com','DOMAIN-SUFFIX,apis.google.com',
 'DOMAIN-SUFFIX,bard.google.com','DOMAIN-SUFFIX,cloudcode-pa.googleapis.com','DOMAIN-SUFFIX,g.ai',
 'DOMAIN-SUFFIX,geller-pa.googleapis.com','DOMAIN-SUFFIX,gemini.google','DOMAIN-SUFFIX,gemini.google.com',
 'DOMAIN-SUFFIX,generativeai.google','DOMAIN-SUFFIX,generativelanguage.googleapis.com',
 'DOMAIN-SUFFIX,makersuite.google.com','DOMAIN-SUFFIX,proactivebackend-pa.googleapis.com',
 'DOMAIN-KEYWORD,alkalimakersuite-pa.clients6.google.com','DOMAIN-KEYWORD,generativelanguage'}
def surge(text):return [l.strip() for l in text.splitlines() if l.strip() and not l.lstrip().startswith('#')]
def syntax(rule):
 p=rule.split(',');assert len(p) in (2,3),f'field count: {rule}'
 typ,val=p[:2];assert typ in TYPES and val and val==val.strip(),f'unsupported rule: {rule}'
 if len(p)==3:assert p[2]=='no-resolve' and typ in {'IP-CIDR','IP-CIDR6','IP-ASN'},f'options: {rule}'
 if typ in {'IP-CIDR','IP-CIDR6'}:
  assert ipaddress.ip_network(val,strict=False).version==(4 if typ=='IP-CIDR' else 6),f'IP family: {rule}'
 elif typ=='IP-ASN':assert val.isdecimal() and 0<int(val)<2**32,f'ASN: {rule}'
 elif typ in {'DOMAIN','DOMAIN-SUFFIX'}:
  assert len(val)<=253 and all(re.fullmatch(r'[A-Za-z0-9_](?:[A-Za-z0-9_-]{0,61}[A-Za-z0-9_])?',part) for part in val.split('.')),f'domain: {rule}'
 elif typ=='DOMAIN-WILDCARD':assert re.fullmatch(r'[A-Za-z0-9_.?*\-]+',val),f'wildcard: {rule}'
 else:assert not any(c in val for c in '\n\r\x00'),f'control character: {rule}'
def matches(rules,domain):
 import fnmatch
 for rule in rules:
  typ,v,*_=rule.split(',')
  if typ=='DOMAIN' and domain==v:return True
  if typ=='DOMAIN-SUFFIX' and (domain==v or domain.endswith('.'+v)):return True
  if typ=='DOMAIN-KEYWORD' and v in domain:return True
  if typ=='DOMAIN-WILDCARD' and fnmatch.fnmatchcase(domain,v):return True
 return False

def validate(baseline=None):
 names={p.stem for p in (ROOT/'Surge').glob('*.list')};assert names==EXPECTED,('Surge inventory',names^EXPECTED)
 assert {p.stem for p in (ROOT/'Mihomo').glob('*.yaml')}==EXPECTED,'Mihomo inventory'
 allrules={};report={}
 for name in sorted(names):
  st=(ROOT/'Surge'/f'{name}.list').read_text();yt=(ROOT/'Mihomo'/f'{name}.yaml').read_text();rules=surge(st);obj=yaml.safe_load(yt)
  assert isinstance(obj,dict) and set(obj)=={'payload'} and obj['payload']==rules,f'paired output mismatch: {name}'
  assert len(rules)==len(set(rules)),f'duplicate: {name}'
  for rule in rules:syntax(rule)
  assert not any(x in st+yt for x in ['<<<<<<<','>>>>>>>','BEGIN PRIVATE KEY','ghp_']),f'unsafe content: {name}'
  allrules[name]=set(rules);row: dict[str,Any]={'count':len(rules)}
  if baseline:
   oldtext=subprocess.check_output(['git','show',f'{baseline}:Surge/{name}.list'],cwd=ROOT,text=True);old=set(surge(oldtext));new=set(rules)
   row.update(added=sorted(new-old),removed=sorted(old-new),before=len(old));row['change_percent']=round((len(new-old)+len(old-new))/max(1,len(old))*100,2)
   if new!=old:
    current_date=re.search(r'# UPDATED: (\d{4}-\d{2}-\d{2})',st);old_date=re.search(r'# UPDATED: (\d{4}-\d{2}-\d{2})',oldtext)
    assert current_date and old_date,name
    assert current_date.group(1)>=old_date.group(1),name
  report[name]=row
 for doc in ['README.md','README.en.md']:
  text=(ROOT/doc).read_text();counts=dict((n,int(c)) for n,c in re.findall(r'\| `([^`]+)` \| `(\d+)` \|',text));assert set(counts)==names,(doc,'inventory')
  assert all(counts[n]==report[n]['count'] for n in names),(doc,'counts')
 assert 'DOMAIN-SUFFIX,oaistatsig.com' in allrules['AI'],'missing OpenAI Statsig domain'
 assert not (allrules['AI']&GEMINI),'Gemini exclusion regression'
 for domain in ['gemini.google.com','bard.google.com','aistudio.google.com','ai.google.dev','generativelanguage.googleapis.com','daily-cloudcode-pa.googleapis.com']:
  assert not matches(allrules['AI'],domain),('AI semantic exclusion',domain)
 for domain in ['icloud.com','icloud.com.cn','icloud-content.com','me.com']:
  assert not matches(allrules['AppleCN'],domain),('AppleCN iCloud exclusion',domain)
 # AWS includes the Amazon consumer ecosystem by explicit user policy.
 for domain in ['amazon.com','primevideo.com']:
  assert matches(allrules['AWS'],domain),('AWS Amazon ecosystem coverage',domain)
 assert 'DOMAIN-SUFFIX,gemini.com' in allrules['Crypto'],'unrelated Gemini exchange removed'
 # Ads follows AWAvenue exactly; unrelated homonyms must not be removed by AI filtering,
 # but an upstream Ads removal must not be blocked by a permanently hardcoded entry.
 subprocess.run(['git','diff','--check'],cwd=ROOT,check=True)
 totals={'rulesets':len(names),'files':len(names)*2,'rules':sum(r['count'] for r in report.values())}
 if baseline:totals.update(added=sum(len(r['added']) for r in report.values()),removed=sum(len(r['removed']) for r in report.values()),changed_rulesets=sum(bool(r['added'] or r['removed']) for r in report.values()))
 return {'passed':True,'totals':totals,'rulesets':report}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--baseline');ap.add_argument('--report');args=ap.parse_args();result=validate(args.baseline)
 if args.report:pathlib.Path(args.report).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'passed':result['passed'],**result['totals']},ensure_ascii=False))
