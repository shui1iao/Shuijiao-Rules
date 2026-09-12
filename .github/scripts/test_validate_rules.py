"""Run with: python3 -m unittest discover -s .github/scripts -p 'test_*.py'."""
import importlib.util
import pathlib
import unittest

spec = importlib.util.spec_from_file_location('validate_rules', pathlib.Path(__file__).with_name('validate-rules.py'))
assert spec and spec.loader
rules = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rules)

class RuleValidationTests(unittest.TestCase):
    def test_supported_syntax(self):
        for rule in ['DOMAIN,api.example.com', 'DOMAIN-SUFFIX,example.com', 'DOMAIN-KEYWORD,openai', 'DOMAIN-WILDCARD,*.example.com', 'IP-CIDR,192.0.2.0/24,no-resolve', 'IP-CIDR6,2001:db8::/32,no-resolve', 'IP-ASN,64512,no-resolve', 'PROCESS-NAME,Example Client']:
            with self.subTest(rule=rule):
                rules.syntax(rule)

    def test_invalid_syntax(self):
        for rule in ['MATCH,Proxy', 'DOMAIN,https://example.com', 'DOMAIN-SUFFIX,.example.com', 'DOMAIN,example..com', 'DOMAIN,example.com,no-resolve', 'IP-ASN,0', 'IP-ASN,4294967296', 'IP-CIDR6,192.0.2.0/24', 'DOMAIN-WILDCARD,(.*).example.com']:
            with self.subTest(rule=rule), self.assertRaises((AssertionError, ValueError)):
                rules.syntax(rule)

    def test_suffix_boundaries(self):
        policy={'DOMAIN-SUFFIX,oaistatsig.com'}
        self.assertTrue(rules.matches(policy,'oaistatsig.com'))
        self.assertTrue(rules.matches(policy,'events.oaistatsig.com'))
        self.assertFalse(rules.matches(policy,'not-oaistatsig.com'))
        self.assertFalse(rules.matches({'DOMAIN-SUFFIX,statsig.com'},'oaistatsig.com'))

    def test_broad_rules_cannot_bypass_exclusion_checks(self):
        self.assertTrue(rules.matches({'DOMAIN-SUFFIX,google.com'},'gemini.google.com'))
        self.assertTrue(rules.matches({'DOMAIN-KEYWORD,amazon'},'amazon.com'))
        self.assertFalse(rules.matches({'DOMAIN-SUFFIX,amazonaws.com'},'amazon.com'))
        self.assertFalse(rules.matches({'DOMAIN-SUFFIX,gemini.com'},'gemini.google.com'))

    def test_surge_comments_and_empty_lines(self):
        self.assertEqual(rules.surge('# NAME: test\n\nDOMAIN,example.com\n'),['DOMAIN,example.com'])

if __name__=='__main__':
    unittest.main()
