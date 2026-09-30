# Privacy Policy — apMZoomAI · Dongdaemun Wholesale (Dify plugin)

Operator: apM Hwashin Co., Ltd. (에이피엠화신 주식회사), 40 Majang-ro, Jung-gu, Seoul, Korea.
Contact: apm@apmzoom.com

## What the plugin itself does with your data

The plugin does not collect, store or log any user data, and it sets no cookies. When a workflow or agent calls one of
its tools, the plugin forwards the tool inputs — search keywords, building, floor, stall number, item id, language and
result limits — over HTTPS to apMZoomAI's public, read-only MCP interface at `https://www.apmzoom.com/mcp` and returns
the answer. It needs no account, API key or credentials, and it sends nothing else.

## What apMZoomAI processes when a request arrives

- **What:** the search words and filters that were sent, and the source IP address.
- **Why:** to return the results and to block excessive requests. The IP address is used only to count requests per
  minute and is deleted when the roughly 60-second counting window ends.
- **Translation:** a non-English search word that apMZoomAI's own glossary cannot handle is sent to an AI model provider
  (OpenAI) to be translated into English, or, failing that, to a backup translation service (MyMemory). The search word
  may therefore reach servers outside Korea. Only the search word and the language pair are sent, nothing that
  identifies you.
- **Temporary cache:** to respond faster, translations of search words, the search values computed from them, and
  lookup results are kept briefly in the cache of apMZoomAI's cloud infrastructure provider (Cloudflare) — translations
  and values for up to 30 days, lookup results for up to 60 minutes. The cache holds nothing that identifies you.
- **Cookies and accounts:** none. The interface has no accounts, sign-in or sessions.
- **Infrastructure logs:** Cloudflare may keep basic request records for a period under its own policies.

Search words sent through this interface are not linked to any user account and are not stored separately in a
database. No sensitive personal data (health, financial, biometric, children's, location or authentication data) is
requested or needed.

## Third parties

OpenAI and MyMemory (translation, as described above) and Cloudflare (hosting and caching). How your Dify deployment or
AI model provider handles your information is governed by their own policies.

## More

The full apMZoomAI privacy policy is at https://www.apmzoom.com/privacy (section 10, "Public MCP interface").
Questions or requests: apm@apmzoom.com.
