# apMZoomAI · Dongdaemun wholesale (MCP server, Agent Skill, Claude plugin)

Search the Dongdaemun wholesale fashion market in Seoul from any AI assistant that speaks the
[Model Context Protocol](https://modelcontextprotocol.io). Find items, see new arrivals, locate stalls by
building, floor and stall number, and open each item or stall on [apMZoomAI](https://www.apmzoom.com).

- **Endpoint:** `https://www.apmzoom.com/mcp`
- **Transport:** Streamable HTTP (stateless, JSON responses)
- **Authentication:** none — the server is public and read-only
- **Languages:** English, 中文, 한국어, 日本語, Tiếng Việt, ไทย, Bahasa Indonesia, Bahasa Melayu

## What it does

| Tool | What it returns |
| --- | --- |
| `search_products` | Wholesale items matching short keywords in any of the eight languages, with photos, category, the stall's building / floor / stall number and an apMZoomAI link |
| `get_new_arrivals` | The newest items uploaded in the last 1–168 hours, optionally filtered by building and category |
| `find_stalls` | Stalls by name or stall number, or by building and floor, with how many items each lists and its store page |
| `get_product` | One item by id: name, up to three photos, category, stall location and link |
| `list_buildings` | The market buildings covered, with stall counts, new items in the last 7 days and, where known, opening hours and address |

All tools are read-only (`readOnlyHint: true`, `destructiveHint: false`, `idempotentHint: true`, `openWorldHint: false`).

**What it does not do:** it never returns prices, discounts, stock levels or merchant contact details, and it cannot
place orders. Buyers open the item or store link on apMZoomAI to see prices and wholesale ordering details.
Only stalls currently in business are included.

## Add it to your assistant

- **Claude (web, desktop, mobile):** Settings → Connectors → Add custom connector → paste `https://www.apmzoom.com/mcp`.
- **Claude Code:** `claude mcp add --transport http apmzoom https://www.apmzoom.com/mcp`,
  or install the plugin from this repository: `/plugin marketplace add apmleokeo-gif/apmzoom-mcp` then `/plugin install apmzoom-dongdaemun@apmzoom`.
- **Cursor:** [Add to Cursor](https://cursor.com/en/install-mcp?name=apmzoom&config=eyJ1cmwiOiJodHRwczovL3d3dy5hcG16b29tLmNvbS9tY3AifQ%3D%3D)
- **VS Code:** [Install in VS Code](https://vscode.dev/redirect/mcp/install?name=apmzoom&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Fwww.apmzoom.com%2Fmcp%22%7D)
- **Gemini CLI:** this repository is also a Gemini CLI extension (`gemini-extension.json`).
- **Dify:** add the URL as an MCP server (Tools → MCP), or use the tool plugin in [`dify-plugin/`](dify-plugin) (submitted to the Dify Marketplace).
- **Any other MCP client:** add a remote server with the URL above; no API key is needed.

## Try asking

- "Find linen dresses from Dongdaemun wholesale stalls."
- "帮我找东大门最近 24 小时上新的针织开衫。"
- "동대문 누존 2층 원피스 매장 찾아줘."
- "東大門で最近入荷したデニムを見せて。"
- "Tìm váy linen bán sỉ ở chợ Dongdaemun."
- "หาเสื้อถักขายส่งที่ตลาดทงแดมุน"
- "Cari gaun linen grosir di pasar Dongdaemun."
- "Cari kardigan kait borong terbaru di Dongdaemun."

## Contents of this repository

- `plugins/apmzoom-dongdaemun/` — Claude plugin: the remote MCP server (`.mcp.json`) plus the `dongdaemun-sourcing` Agent Skill
- `.claude-plugin/marketplace.json` — lets Claude Code add this repository as a plugin marketplace
- `server.json` — the listing in the official MCP Registry (`com.apmzoom.www/dongdaemun`)
- `gemini-extension.json`, `GEMINI.md` — Gemini CLI extension
- `dify-plugin/` — Dify tool plugin source (five tools wrapping the same server; no credentials)
- `plugin.json`, `mcp.json`, `skills/` — the repository root is also an [Agent Plugin](https://agent-plugins.org) (the format Kiro Powers and other clients read): manifest, the remote MCP server, and the same `dongdaemun-sourcing` skill

The server itself is operated by apM Hwashin Co., Ltd. and is not part of this repository.

## Data and privacy

No account or sign-in is needed. Requests are rate-limited per network address. Search keywords may be processed by an
AI translation service to match items listed in other languages. Item names and photos come from the stalls that list them.

- Privacy policy: https://www.apmzoom.com/privacy
- Terms: https://www.apmzoom.com/terms

## Support and security

Questions, problems or security reports: apm@apmzoom.com (for security issues, please put "Security" in the subject).

Operated by apM Hwashin Co., Ltd. (에이피엠화신 주식회사), 40 Majang-ro, Jung-gu, Seoul, Korea.
