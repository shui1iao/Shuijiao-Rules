# Shuijiao-Rules

[English](README.en.md)

水饺自用的 Surge / Mihomo 分流规则。仓库只保留两个规则目录：`Surge/` 和 `Mihomo/`。

- 主要参考：[`SukkaW/Surge`](https://github.com/SukkaW/Surge)、[`blackmatrix7/ios_rule_script`](https://github.com/blackmatrix7/ios_rule_script) 与 [`v2fly/domain-list-community`](https://github.com/v2fly/domain-list-community)
- 补充交叉核对：[`ACL4SSR/ACL4SSR`](https://github.com/ACL4SSR/ACL4SSR)、[`MetaCubeX/meta-rules-dat`](https://github.com/MetaCubeX/meta-rules-dat)；按分类补缺，不无条件合并全部上游规则，共同上游不视为独立佐证
- 去广告规则：`Ads` 来源于 [`TG-Twilight/AWAvenue-Ads-Rule`](https://github.com/TG-Twilight/AWAvenue-Ads-Rule)，推荐搭配 `REJECT` 策略使用
- 输出格式：Surge 使用 `.list`，Mihomo 使用 `behavior: classical` 的 `.yaml`
- 内容一致：同名的 Surge 与 Mihomo 文件使用同一份规则内容，只是文件格式不同
- CDN 规则：已经合并进 `Proxy`，不单独提供 `CDN` 文件
- MTProto DC 配置：使用 Surge 官方生成器每日自动更新 `Surge/mtproto-dc-config.json`
- 更新时间：`2026-09-13`

## 规则列表

| 规则 | 条数 | Surge | Mihomo |
|---|---:|---|---|
| `Telegram` | `54` | `Surge/Telegram.list` | `Mihomo/Telegram.yaml` |
| `GitHub` | `60` | `Surge/GitHub.list` | `Mihomo/GitHub.yaml` |
| `AWS` | `245` | `Surge/AWS.list` | `Mihomo/AWS.yaml` |
| `AI` | `386` | `Surge/AI.list` | `Mihomo/AI.yaml` |
| `Speedtest` | `1252` | `Surge/Speedtest.list` | `Mihomo/Speedtest.yaml` |
| `Crypto` | `364` | `Surge/Crypto.list` | `Mihomo/Crypto.yaml` |
| `Google` | `954` | `Surge/Google.list` | `Mihomo/Google.yaml` |
| `Apple` | `187` | `Surge/Apple.list` | `Mihomo/Apple.yaml` |
| `AppleCN` | `8` | `Surge/AppleCN.list` | `Mihomo/AppleCN.yaml` |
| `Proxy` | `12525` | `Surge/Proxy.list` | `Mihomo/Proxy.yaml` |
| `China` | `7884` | `Surge/China.list` | `Mihomo/China.yaml` |
| `Douyin` | `77` | `Surge/Douyin.list` | `Mihomo/Douyin.yaml` |
| `LAN` | `172` | `Surge/LAN.list` | `Mihomo/LAN.yaml` |
| `Ads` | `952` | `Surge/Ads.list` | `Mihomo/Ads.yaml` |
| `Streaming` | `1939` | `Surge/Streaming.list` | `Mihomo/Streaming.yaml` |
| `Game` | `757` | `Surge/Game.list` | `Mihomo/Game.yaml` |
| `Pay` | `495` | `Surge/Pay.list` | `Mihomo/Pay.yaml` |

## 分类说明

- `Telegram`：Telegram 域名、ASN/IP 段。
- `GitHub`：GitHub、GitHub Assets/UserContent、GitHub Container Registry、npm 相关域名。
- `AWS`：Amazon Web Services 全球及中国区域名，以及亚马逊购物、Prime Video 等 Amazon 生态；包括 AWS 控制台与文档、Amazon API 域名、CloudFront、Amplify、Elastic Beanstalk、Cognito、SES 等。
- `AI`：OpenAI / ChatGPT / Claude / Grok / Perplexity / Poe / Copilot / Midjourney / Hugging Face / Mistral / Cursor / Windsurf 等 AI 服务；不包含 Gemini、Bard、AI Studio 与 Gemini API。
- `Speedtest`：Ookla Speedtest、Fast、Cloudflare Speed、M-Lab、LibreSpeed 以及常见测速节点。
- `Crypto`：Binance、Bybit、OKX、Coinbase、Kraken、KuCoin、Gate、MEXC、Bitget、HTX/Huobi、行情、钱包、DeFi 与链上浏览器。
- `Google`：Google、YouTube、Gmail、Drive、Firebase 等常规 Google 服务；Gemini / AI Studio 不再放入 `AI`，将按后续 `Google` / `Proxy` 规则处理。
- `Apple`：Apple 国际服务、Apple Media、Apple TV、Apple Developer、Apple CDN 与 Apple IP。
- `AppleCN`：参考 Sukka 的中国区 Apple 规则，但刻意移除 iCloud；建议直连。
- `Proxy`：常见国外站点、国外 CDN、开发者服务、社交服务等；已合并 CDN。
- `China`：中国大陆常见域名、关键词与 BGP IP 段，建议直连。
- `Douyin`：备用抖音规则，覆盖抖音、抖音电商、抖音 CDN/视频域名；这是国内抖音，不是国际版 TikTok。
- `LAN`：局域网、本地域名、私有地址段，建议直连。
- `Ads`：轻量去广告规则，来源于 AWAvenue Ads Rule；不合并其它大体量拦截集合，以控制误杀风险。
- `Streaming`：备用流媒体规则，覆盖 Netflix、Disney+、HBO/Max、Prime Video、Spotify、YouTube/YouTube Music、Hulu、Twitch、TikTok 等。
- `Game`：备用游戏平台规则，覆盖 Steam、Epic、Battle.net、Xbox、PlayStation、Nintendo、EA、Ubisoft、Riot、Rockstar、GeForce Now 等。
- `Pay`：备用传统支付规则，覆盖 PayPal、Stripe、Wise、Revolut、Visa、Mastercard、American Express、Payoneer、Airwallex 等。

## 推荐优先级

当前常用配置可以只引用主规则，备用规则按需插入：

```text
LAN     -> DIRECT
Ads     -> REJECT
AppleCN -> DIRECT
China   -> DIRECT
AI      -> AI / Proxy
Telegram-> Telegram / Proxy
GitHub  -> GitHub / Proxy
AWS     -> AWS / Proxy
Crypto  -> Crypto / Proxy
Speedtest -> Proxy
Google  -> Proxy
Apple   -> Proxy
Proxy   -> Proxy
FINAL/MATCH -> Proxy
```

备用规则建议策略：

```text
Douyin   -> DIRECT / Final
Streaming -> Final / Streaming
Game      -> Final / Game
Pay       -> Final / Pay
```

优先级原则：`LAN` 永远最前；`Ads` 放在 `China` 前面，避免国内广告域名被直连规则提前命中；`AppleCN` 早于 `Apple`；`AI` 早于 `Google` / `Proxy`；`GitHub`、`AWS` 早于 `Proxy`；具体分类早于 `Proxy`。备用规则不默认启用，避免当前配置变复杂。

## Surge 示例

```ini
[Rule]
RULE-SET,https://raw.githubusercontent.com/shui1iao/Shuijiao-Rules/main/Surge/LAN.list,DIRECT
RULE-SET,https://raw.githubusercontent.com/shui1iao/Shuijiao-Rules/main/Surge/Ads.list,REJECT
RULE-SET,https://raw.githubusercontent.com/shui1iao/Shuijiao-Rules/main/Surge/AppleCN.list,DIRECT
RULE-SET,https://raw.githubusercontent.com/shui1iao/Shuijiao-Rules/main/Surge/China.list,DIRECT
RULE-SET,https://raw.githubusercontent.com/shui1iao/Shuijiao-Rules/main/Surge/AI.list,AI
RULE-SET,https://raw.githubusercontent.com/shui1iao/Shuijiao-Rules/main/Surge/Telegram.list,Telegram
RULE-SET,https://raw.githubusercontent.com/shui1iao/Shuijiao-Rules/main/Surge/GitHub.list,GitHub
RULE-SET,https://raw.githubusercontent.com/shui1iao/Shuijiao-Rules/main/Surge/AWS.list,AWS
RULE-SET,https://raw.githubusercontent.com/shui1iao/Shuijiao-Rules/main/Surge/Crypto.list,Crypto
RULE-SET,https://raw.githubusercontent.com/shui1iao/Shuijiao-Rules/main/Surge/Speedtest.list,Proxy
RULE-SET,https://raw.githubusercontent.com/shui1iao/Shuijiao-Rules/main/Surge/Google.list,Proxy
RULE-SET,https://raw.githubusercontent.com/shui1iao/Shuijiao-Rules/main/Surge/Apple.list,Proxy
RULE-SET,https://raw.githubusercontent.com/shui1iao/Shuijiao-Rules/main/Surge/Proxy.list,Proxy
FINAL,Proxy
```

## Surge MTProto DC 配置

仓库每天北京时间 03:17 使用 [`surge-networks/MTProtoDCConfigGenerator`](https://github.com/surge-networks/MTProtoDCConfigGenerator) 官方生成器，从 Telegram `help.getConfig` 生成生产 DC 地址映射。生成结果通过格式、字段和 256 KiB 大小检查后才会提交。

```ini
[MTProto]
dc-config-url = https://raw.githubusercontent.com/shui1iao/Shuijiao-Rules/refs/heads/main/Surge/mtproto-dc-config.json
```

该文件只负责将 Telegram DC 编号映射为当前生产端点，不代替 Surge 分流规则。完整格式和缓存行为见 [Surge MTProto 官方文档](https://manual.nssurge.com/others/mtproto.html)。

## Mihomo 示例

```yaml
rule-providers:
  ai:
    type: http
    behavior: classical
    format: yaml
    interval: 86400
    path: ./rules/Shuijiao/AI.yaml
    url: https://raw.githubusercontent.com/shui1iao/Shuijiao-Rules/main/Mihomo/AI.yaml

rules:
  - RULE-SET,ai,AI
  - MATCH,Proxy
```

## 多源维护与校验

- 每次逐项检查全部 17 个规则集；无有效差异的文件保留原日期，不为凑更新而改动。
- [来源清单与分类策略](.github/rules-maintenance.json) 记录来源 URL、快照哈希、分类覆盖和审查决定。补充源用于查漏，不等于全量并集；既有人工策略优先。
- 2026-09-12 全量复核：16 类有内容变化，`AppleCN` 核对后保持不变；补齐 `oaistatsig.com`。`AWS` 已纳入购物和 Prime Video 域名，但不将整个云租户 IP 目录无条件归入该域名分类。
- 大幅变化需逐项复核；自动维护遇到单类增删超过 20% 或全仓净变化超过 500 条仍停止发布，不因本次扩源而关闭保护。
- 校验覆盖规则语法、双格式顺序一致、去重、文档计数及人工排除项；不等同于真实设备的端到端流量测试。

```bash
# 需要 Python 3 和 PyYAML
python3 -B .github/scripts/validate-rules.py
python3 -B -m unittest discover -s .github/scripts -p 'test_*.py'
```

## 来源与授权

本仓库为个人自用规则整理，不声明上游规则原创权。规则主要来自并参考：

- [`SukkaW/Surge`](https://github.com/SukkaW/Surge)
- [`blackmatrix7/ios_rule_script`](https://github.com/blackmatrix7/ios_rule_script)
- [`v2fly/domain-list-community`](https://github.com/v2fly/domain-list-community)
- [`ACL4SSR/ACL4SSR`](https://github.com/ACL4SSR/ACL4SSR)
- [`MetaCubeX/meta-rules-dat`](https://github.com/MetaCubeX/meta-rules-dat)
- [`TG-Twilight/AWAvenue-Ads-Rule`](https://github.com/TG-Twilight/AWAvenue-Ads-Rule)

本仓库仅做格式转换、去重、合并和个人补丁维护。使用前请自行确认上游项目的授权、免责声明和适用范围。
