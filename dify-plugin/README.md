# apMZoomAI · Dongdaemun Wholesale

Search the Dongdaemun wholesale fashion market in Seoul from a Dify workflow or agent. Find items, see new
arrivals, and locate stalls by building, floor and stall number — every result links back to
[apMZoomAI](https://www.apmzoom.com), where buyers see prices and wholesale ordering details.

The plugin is a thin wrapper around apMZoomAI's public, read-only
[MCP](https://modelcontextprotocol.io) server at `https://www.apmzoom.com/mcp`.

Source: https://github.com/apmleokeo-gif/apmzoom-mcp/tree/main/dify-plugin

## Tools

| Tool | What it returns |
| --- | --- |
| **Search wholesale items** | Items matching short keywords in any of eight languages, with photos, category, the stall's building / floor / stall number and an apMZoomAI link |
| **New arrivals** | The newest items uploaded in the last 1–168 hours, optionally filtered by building and category |
| **Find stalls** | Stalls by name or stall number, or by building and floor, with item counts and the store page link |
| **Item details** | One item by id: name, up to three photos, category, stall location and link |
| **List buildings** | The market buildings covered, with stall counts, new items in the last 7 days and, where known, opening hours and address |

Item names and labels come back in English, Chinese, Korean, Japanese, Vietnamese, Thai, Indonesian or
Malay (the `lang` input). All tools are read-only.

**What it does not do:** it never returns prices, discounts, stock levels or merchant contact details, and it cannot be used to
buy anything. Only stalls currently in business are included.

## Setup

1. Install the plugin. There is nothing to configure.
2. Add any of the five tools to a workflow (Tool node) or to an Agent app.

**Credentials / APIs:** none. No account, sign-in or API key is required.

**Connection requirements:** the Dify plugin runtime must be able to make outbound HTTPS requests to
`www.apmzoom.com` (port 443). Requests are rate-limited per network address by apMZoomAI.

## Usage examples

- Agent prompt: "Find linen dresses from Dongdaemun wholesale stalls, then show the stall locations."
- Workflow: *Search wholesale items* (`query` = `knit cardigan`, `building` = `THEOT`, `limit` = 5) → LLM node that
  summarises the `text` output for a buyer.
- Workflow: *List buildings* → pick a building key → *New arrivals* (`building` = that key, `hours` = 24).

Building keys (for the `building` input) come from *List buildings*, for example `apM`, `THEOT`, `NUZZON`. Short forms
such as a display name or a unique prefix are also accepted.

Prefer not to install a plugin? Dify can also connect to the same server through its built-in MCP support using the
URL `https://www.apmzoom.com/mcp` (no authentication).

## Outputs

Each tool returns a text message (what an agent reads) and a JSON message with the same data in structured form
(`products`, `stalls` or `buildings`, plus a `note`). Errors such as "item no longer listed" come back as text so an
agent can react; network failures raise a tool error.

## Data and privacy

See [PRIVACY.md](PRIVACY.md). In short: the plugin itself collects and stores nothing; the search words and filters you
send are processed by apMZoomAI's public MCP server, which needs no account.

## Support

Questions, problems or security reports: apm@apmzoom.com (for security issues, put "Security" in the subject).
Operated by apM Hwashin Co., Ltd. (에이피엠화신 주식회사), 40 Majang-ro, Jung-gu, Seoul, Korea.
