# AI Stock Analysis System

**AI-powered stock analysis system for A-shares / Hong Kong / US / Japanese / Korean stocks**

Analyze your watchlist daily → generate a decision dashboard → push to Telegram / Discord / Slack / Email / WeChat Work / Feishu.

[**Quick Start**](#-quick-start) · [**Sample Output**](#-sample-output) · [**Documentation Index**](docs/INDEX_EN.md) · [**Full Guide**](docs/full-guide_EN.md)

English | [繁體中文](docs/README_CHT.md)

## 🖥️ Product Preview

<p align="center">
  <img src="docs/assets/readme_workspace_tour_20260510.gif" alt="DSA Web workspace demo" width="720">
</p>

## ✨ Key Features

| Capability | Coverage |
|------------|----------|
| AI decision reports | Core conclusion, score, trend, entry/exit levels, risk alerts, catalysts, and action checklist |
| Multi-market data | A-shares, Hong Kong, US, ETFs: quotes, K-lines, technical indicators, capital flow, chips, news, announcements, and fundamentals; Japanese/Korean (Yahoo `.T` / `.KS` / `.KQ`): currently MVP supports YFinance basic/quote + daily data and technical indicators only, while capital flow, dragon_tiger, boards, and related advanced blocks may return `not_supported` (see [market boundaries](docs/market-support.md)) |
| Web / desktop workspace | Manual analysis, task progress, history, full Markdown reports, backtest, portfolio, settings, and light/dark themes |
| Agent strategy chat | Multi-turn Q&A with 15 built-in strategies across Web/Bot/API |
| Smart import & autocomplete | Image, CSV/Excel, clipboard import; code/name/pinyin/alias autocomplete |
| Automation & notifications | GitHub Actions, Docker, local scheduler, FastAPI service, and WeChat Work / Feishu / Telegram / Discord / Slack / Email delivery |

> Detailed fields, fundamental P0 timeout semantics, trading rules, data-source priority, Web/API behavior, and troubleshooting live in the [Full Guide](docs/full-guide_EN.md).

### Tech Stack & Data Sources

| Type | Supported |
|------|-----------|
| AI Models | [Anspire](https://open.anspire.cn/?share_code=QFBC0FYC), [AIHubMix](https://aihubmix.com/?aff=CfMq), Gemini, OpenAI-compatible providers, DeepSeek, Qwen, Claude, Ollama |
| Market Data | [TickFlow](https://tickflow.org/auth/register?ref=WDSGSPS5XC), AkShare, Tushare, Pytdx, Baostock, YFinance, Longbridge |
| News Search | [Anspire](https://open.anspire.cn/?share_code=QFBC0FYC), [SerpAPI](https://serpapi.com/baidu-search-api?utm_source=github_daily_stock_analysis), [Tavily](https://tavily.com/), [Bocha](https://open.bocha.cn/), [Brave](https://brave.com/search/api/), [MiniMax](https://platform.minimaxi.com/), SearXNG |
| Social Sentiment | [Stock Sentiment API](https://api.adanos.org/docs) for Reddit / X / Polymarket, US stocks only |

## 🚀 Quick Start

### Option 1: GitHub Actions (Recommended)

> Deploy in about 5 minutes, with no server and no infrastructure cost.

#### 1. Fork this repository

Click `Fork` in the upper-right corner. A star is very welcome if this project helps you.

#### 2. Configure Secrets

Open your forked repository, then go to `Settings` → `Secrets and variables` → `Actions` → `New repository secret`.

**AI model configuration (configure at least one)**

| Secret Name | Description | Required |
|-------------|-------------|:--------:|
| `ANSPIRE_API_KEYS` | [Anspire](https://open.anspire.cn/?share_code=QFBC0FYC) API key | **Recommended** |
| `AIHUBMIX_KEY` | [AIHubMix](https://aihubmix.com/?aff=CfMq) API key | **Recommended** |
| `GEMINI_API_KEY` | Google Gemini API key | Optional |
| `ANTHROPIC_API_KEY` | Anthropic Claude API key | Optional |
| `OPENAI_API_KEY` | OpenAI-compatible API key, including DeepSeek and Qwen-compatible services | Optional |
| `OPENAI_BASE_URL` / `OPENAI_MODEL` | Fill these when using an OpenAI-compatible provider | Optional |

**Watchlist (required)**

| Secret Name | Description | Required |
|-------------|-------------|:--------:|
| `STOCK_LIST` | Watchlist codes, e.g. `600519,hk00700,AAPL,7203.T,005930.KS` | ✅ |

**Notification channels (configure at least one)**

| Secret Name | Description |
|-------------|-------------|
| `WECHAT_WEBHOOK_URL` | WeChat Work bot |
| `FEISHU_WEBHOOK_URL` | Feishu bot |
| `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` | Telegram |
| `DISCORD_WEBHOOK_URL` | Discord webhook |
| `SLACK_BOT_TOKEN` + `SLACK_CHANNEL_ID` | Slack bot |
| `EMAIL_SENDER` + `EMAIL_PASSWORD` | Email push |

#### 3. Enable Actions

Open the `Actions` tab and click `I understand my workflows, go ahead and enable them`.

#### 4. Manual Test

`Actions` → `Daily Stock Analysis` → `Run workflow` → `Run workflow`.

#### Done

By default, the workflow runs every weekday at 18:00 Beijing time and skips non-trading days.

### Option 2: Local / Docker Deployment

```bash
git clone https://github.com/ZhuLinsen/daily_stock_analysis.git && cd daily_stock_analysis
pip install -r requirements.txt
cp .env.example .env && vim .env
python main.py
```

```bash
python main.py --debug
python main.py --stocks 600519,hk00700,AAPL
python main.py --market-review
python main.py --schedule
python main.py --webui
```

## 📱 Sample Output

```markdown
🎯 2026-02-08 Decision Dashboard
Analyzed 3 stocks | 🟢 Buy:0 🟡 Watch:2 🔴 Sell:1

📊 Summary
🟡 000657: Watch | Score 65 | Bullish
🟡 600105: Watch | Score 48 | Range-bound
🔴 300260: Sell | Score 35 | Bearish

🚨 Risk Alerts:
Risk 1: Main-force funds showed notable outflow.
Risk 2: Chip concentration suggests short-term resistance.

✨ Positive Catalysts:
Catalyst 1: AI-server supply-chain exposure remains a market focus.
Catalyst 2: Recent earnings growth provides fundamental support.
```

## ⚙️ Configuration

Full environment variables, model routing, notification channels, data-source priority, trading rules, fundamental P0 semantics, and deployment details are in the [Full Guide](docs/full-guide_EN.md).

## 🖥️ Web UI

```bash
python main.py --webui
python main.py --webui-only
```

Visit `http://127.0.0.1:8000`.

## 🤖 Agent Strategy Chat

After configuring any available AI API key, the Web `/chat` page can use strategy chat.

- Built-in strategies include moving-average crossovers, Chan theory, Elliott wave, bull trend, hot themes, event-driven, growth quality, expectation repricing, and more
- Calls realtime quotes, K-line data, technical indicators, news, and risk context
- Supports follow-up questions, session export, notification sending, and background execution

## 📄 License

[MIT License](LICENSE) © 2026 ZhuLinsen

## ⚠️ Disclaimer

This project is for informational and educational purposes only. AI-generated analysis is not investment advice. Stock market investing involves risk; do your own research and consult a licensed financial advisor when needed.
