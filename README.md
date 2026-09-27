# meta-top

Region-aware Meta ads deep-research skill. Find winning digital products in the Meta ecosystem for one of six v1 regions (India, US, Canada, UK, Australia, UAE) with concrete pricing tiers, creative angles, and Meta-format-compliant ad-copy templates.

> **Trust + ethics frame baked in.** `meta-top` is a competitive-landscape research tool — it surfaces winning categories and positioning gaps so you can build your *original* product with a sharper angle. It does **not** recommend cloning specific creator content. Option B ends with: *"Category design, not content cloning. Find a proven category, identify a positioning gap, create YOUR original product, position with a USP, test small-budget Meta ads, scale what works."*

## What this skill does

`/meta-top <region>` produces a structured six-section deep-research report:

1. **Market snapshot** — region size, Meta share of digital ad spend, 12-month growth direction, regulatory headline.
2. **Top 5–7 product categories** with local-currency pricing examples (₹ / $ / CAD / £ / AUD / AED).
3. **Winning ad creative patterns** — hook type × Meta format (FB primary text, IG Reels, carousel, WA status, collection).
4. **Specific product examples** currently running in the region (observational data, not recommendations).
5. **Meta ad cost benchmarks** (CPM / CPC / CPV in local currency) with `[n sources]` per value.
6. **Option B actionable brief** — pricing tiers (entry / mid / premium), creative angles (2–3 distinct hooks), Meta-format-compliant ad-copy templates (FB primary text ≤125 chars, headline ≤40 chars, IG Reels 9:16 ≤15 sec, WA status 24h ephemeral).

Optional flags:

- `--category <name>` — narrow output to a single product category.
- `--emit=html` — write a self-contained HTML brief alongside the chat output.

## Supported regions (v1)

| Code | Region | Currency | Regulatory anchor |
|------|--------|----------|-------------------|
| `in` | India | INR (₹) | ASCI / MeitY |
| `us` | United States | USD ($) | FTC / FDA / CCPA |
| `ca` | Canada | CAD | Ad Standards / CRTC |
| `uk` | United Kingdom | GBP (£) | ASA / ICO |
| `au` | Australia | AUD | ACMA / AANA |
| `ae` | United Arab Emirates | AED | NMC / TDRA |

Any other region triggers an explicit "region not in v1" response with a recommendation to open an upstream issue.

## What's in this repo

```
skills/
└── meta-top/
    ├── SKILL.md                              # orchestrator (SKILL + voice + output contract + source ladder)
    ├── references/
    │   ├── regions/{in,us,ca,uk,au,ae}.yaml  # curated region anchors + top_brands per region (v1.1)
    │   └── agents/meta-top-researcher.md     # live-research sub-agent (walks the source ladder, v1.1)
    └── scripts/                              # v1.1 keyless DDG floor
        ├── keyless_search.py                 # CLI entry point (Bash-callable by sub-agent)
        ├── lib/
        │   ├── __init__.py                   # bare package marker (mirrors last30days rule)
        │   ├── http.py                       # stdlib HTTP w/ retry + backoff
        │   └── web_search_keyless.py         # DuckDuckGo HTML + optional SearXNG
        └── test_keyless_search.py            # smoke test (skips on network-empty)
```

The skill mirrors the `last30days` deep-research pattern (badge line, voice contract as guaranteed-load band, pre-flight checks, per-region Resolved block, inline `[name](url)` citations, multi-source fallback ladder) and the `ce-product-pulse` hybrid pattern (curated region config + live research layer). Sub-agent architecture follows `ce-slack-research`.

## Reliability (v1.1+)

When the host's WebSearch tool is unavailable or returns empty payloads, meta-top does NOT fail outright. The sub-agent walks a transparent 4-tier source ladder:

1. **Host-native WebSearch** — primary.
2. **Keyless DDG/SearXNG** — `python scripts/keyless_search.py "QUERY" --count 5` (stdlib-only; no API keys, no recurring cost). Mirrors last30days's `web_search_keyless.py` pattern.
3. **Curated `top_brands`** — direct WebFetch to each brand-domain URL in the region YAML's `top_brands` list (mamaearth.in, boat-lifestyle.com, phonepe.com, upgrad.com, etc.).
4. **Curated anchors only** — final fallback. Brief still ships; `data_quality_note` flags the limitation.

When tier 2 or 3 contributes any source, `partial_research: true` and the `data_quality_note` records which tier filled the gap. No silent substitution. v1.1 added this after the v1 smoke-test surfaced WebSearch's empty-payload failure mode.

## Trust + ethics

- Specific creator brands appear only as observational data in Sections (b)–(e), never as recommendations.
- The sub-agent filters out MLM recruitment signals, unsubstantiated health/financial claims, payday-lending, get-rich-quick income claims, crypto-token-presale mechanics, and unlicensed financial advisory. Excluded patterns are surfaced in a `filtered_patterns` footer so the user sees the boundary.
- Option B is reframed as "category design, not content cloning."

## Origin

This skill was extracted from a planning session on 2026-09-27 and shaped by compound-engineering-plugin research-skill conventions. It now ships standalone under the `meta-top` name (the `ce-` prefix is a compound-engineering-internal convention and would mislead users discovering the skill outside that plugin). A future upstream PR into the CE plugin could re-adopt the `ce-` prefix per CE AGENTS.md.

## License

MIT.
