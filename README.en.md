# Shuijiao-Rules

Personal Surge / Mihomo routing rules for Shuijiao. The repository intentionally keeps only two rule directories: `Surge/` and `Mihomo/`.

- Main references: [`SukkaW/Surge`](https://github.com/SukkaW/Surge), [`blackmatrix7/ios_rule_script`](https://github.com/blackmatrix7/ios_rule_script), and [`v2fly/domain-list-community`](https://github.com/v2fly/domain-list-community)
- `Ads` is sourced from [`TG-Twilight/AWAvenue-Ads-Rule`](https://github.com/TG-Twilight/AWAvenue-Ads-Rule) and is intended to be used with a `REJECT` policy
- Surge outputs `.list`; Mihomo outputs `behavior: classical` `.yaml`
- Same content: files with the same name share the same normalized rules; only the wrapper format differs
- CDN is merged into `Proxy`
- MTProto DC mapping: `Surge/mtproto-dc-config.json` is regenerated daily with Surge's official generator
- Updated: `2026-08-19`

## Rule files

| Rule | Count | Surge | Mihomo |
|---|---:|---|---|
| `Telegram` | `50` | `Surge/Telegram.list` | `Mihomo/Telegram.yaml` |
| `GitHub` | `36` | `Surge/GitHub.list` | `Mihomo/GitHub.yaml` |
| `AWS` | `78` | `Surge/AWS.list` | `Mihomo/AWS.yaml` |
| `AI` | `139` | `Surge/AI.list` | `Mihomo/AI.yaml` |
| `Speedtest` | `128` | `Surge/Speedtest.list` | `Mihomo/Speedtest.yaml` |
| `Crypto` | `239` | `Surge/Crypto.list` | `Mihomo/Crypto.yaml` |
| `Google` | `751` | `Surge/Google.list` | `Mihomo/Google.yaml` |
| `Apple` | `183` | `Surge/Apple.list` | `Mihomo/Apple.yaml` |
| `AppleCN` | `8` | `Surge/AppleCN.list` | `Mihomo/AppleCN.yaml` |
| `Proxy` | `7439` | `Surge/Proxy.list` | `Mihomo/Proxy.yaml` |
| `China` | `7640` | `Surge/China.list` | `Mihomo/China.yaml` |
| `Douyin` | `30` | `Surge/Douyin.list` | `Mihomo/Douyin.yaml` |
| `LAN` | `145` | `Surge/LAN.list` | `Mihomo/LAN.yaml` |
| `Ads` | `905` | `Surge/Ads.list` | `Mihomo/Ads.yaml` |
| `Streaming` | `1852` | `Surge/Streaming.list` | `Mihomo/Streaming.yaml` |
| `Game` | `689` | `Surge/Game.list` | `Mihomo/Game.yaml` |
| `Pay` | `380` | `Surge/Pay.list` | `Mihomo/Pay.yaml` |

## Recommended order

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

Optional standby rules:

```text
Douyin   -> DIRECT / Final
Streaming -> Final / Streaming
Game      -> Final / Game
Pay       -> Final / Pay
```

`GitHub` covers GitHub, GitHub Assets/UserContent, GitHub Container Registry, and npm-related domains. `AWS` covers Amazon Web Services global and China domains, including the AWS console and documentation, Amazon API endpoints, CloudFront, Amplify, Elastic Beanstalk, Cognito, and SES; it intentionally excludes Amazon Shopping and Prime Video. `AI` excludes Gemini, Bard, AI Studio, and the Gemini API; those requests fall through to the later `Google` / `Proxy` rules. `China` includes domains, keywords, and China BGP CIDR rules. `Douyin` is for the mainland Douyin app and related CDN/video domains, not international TikTok. `AppleCN` intentionally excludes iCloud. `Ads` uses AWAvenue only and avoids larger blocklists to reduce false positives. `Douyin`, `Streaming`, `Game`, and `Pay` are provided as optional standby rules and are not meant to be enabled by default.

## Surge MTProto DC configuration

At 03:17 China Standard Time every day, this repository runs the official [`surge-networks/MTProtoDCConfigGenerator`](https://github.com/surge-networks/MTProtoDCConfigGenerator) against Telegram's `help.getConfig`. The result is committed only after schema, field, and 256 KiB size validation.

```ini
[MTProto]
dc-config-url = https://raw.githubusercontent.com/shui1iao/Shuijiao-Rules/refs/heads/main/Surge/mtproto-dc-config.json
```

This file maps Telegram DC IDs to current production endpoints; it does not replace Surge routing rules. See the [official Surge MTProto documentation](https://manual.nssurge.com/others/mtproto.html) for the complete format and cache behavior.

## Attribution

This repository is a personal ruleset aggregation. It does not claim authorship of upstream rules. Main references:

- [`SukkaW/Surge`](https://github.com/SukkaW/Surge)
- [`blackmatrix7/ios_rule_script`](https://github.com/blackmatrix7/ios_rule_script)
- [`v2fly/domain-list-community`](https://github.com/v2fly/domain-list-community)
- [`TG-Twilight/AWAvenue-Ads-Rule`](https://github.com/TG-Twilight/AWAvenue-Ads-Rule)

Please review upstream licenses and disclaimers before use.
