---
name: meta-top
description: "Region-aware deep-research report on best-selling digital products in the Meta ecosystem (Facebook, Instagram, WhatsApp Business) for a specific region. Six regions in v1: india, us, ca, uk, au, ae. Optionally narrows by product category and produces an Option B actionable brief (pricing tiers, creative angles, Meta-format-compliant ad-copy templates). Use when asked for top-selling digital products on Meta, what to launch in a region, what ad creative is working, or what CPM/CPC to budget on Meta in a region."
argument-hint: "<region: in|us|ca|uk|au|ae> [--category NAME] [--emit=html]"
allowed-tools:
  - Read
  - Write
  - WebSearch
  - WebFetch
  - Glob
  - Grep
  - AskUserQuestion
  - Skill
  - Agent
---

# Meta Top — Region-Aware Meta Ads Deep-Research

**Note: The current year is 2026.** Use this when pricing examples, ad-creative patterns, and regulatory notes touch dates or recency claims.

`meta-top` is a region-aware deep-research skill that produces a structured six-section report on best-selling digital products in the Meta ecosystem for one of six v1 regions (India, US, Canada, UK, Australia, UAE), plus an Option B actionable brief (pricing tiers, creative angles, Meta-format-compliant ad-copy templates). Trust + ethics frame baked in: category design, not content cloning. Cloning of specific creator content is **never** the recommendation — the skill surfaces winning categories and positioning gaps so the user can build their *original* product with a sharper angle.

## SKILL CONTRACT (do not improvise)

A `/meta-top <region>` invocation is complete when:

1. Line 1 of the output is the badge: `📊 meta-top v{X} · region: {region} · {YYYY-MM-DD}`. `{X}` is this skill's version (currently `v1.3`); bump it intentionally when shipping breaking changes, never auto-increment per invocation. v1.3 ships the winning-product framework (per-category X/14 rubric, underground-signals callout, 5-option post-menu).
2. The six canonical sections are present in this order: (a) Market snapshot, (b) Top 5–7 product categories with local-currency pricing, (c) Winning ad creative patterns, (d) Specific product examples, (e) Meta ad cost benchmarks (CPM/CPC/CPV in the region's local currency), (f) Option B actionable brief.
3. Every price reference is in the region's local currency (₹ / $ / CAD / £ / AUD / AED). USD is permitted as a secondary annotation only when ground-truth sources report USD (rare); never silently convert.
4. Every citation is inline `[name](url)` markdown. **No raw URLs. No trailing Sources block. No broken empty `[]()` links.** URLs use `http://` or `https://`; `javascript:`, `data:`, `file:` are rejected.
5. Regulatory notes for the region are surfaced explicitly (never silently dropped). At least one para or blockquote per output cites the regulatory body (ASCI for India, FTC for US, ASA for UK, AANA for AU, Ad Standards + CRTC for CA, NMC + TRA for UAE).
6. A trust + ethics one-liner appears under Option B: **"Category design, not content cloning. Find a proven category, identify a positioning gap, create YOUR original product, position with a USP, test small-budget Meta ads, scale what works."**
7. `data_freshness_note` and `data_quality_note` appear under Section (b) when the live research surfaces thin data or rate-limit / partial-research conditions. Honest caveats are load-bearing output, not optional polish.
8. After Option B, a post-menu is presented inline via the platform's blocking question tool with these **five** options: (1) drill into a specific category with a follow-up `/meta-top <region> --category=<name>`, (2) save a self-contained HTML brief via `--emit=html`, (3) export the Option B creative pack as a paste-ready Markdown block, (4) **winning-product dashboard** — render section-(b) categories ranked by `winning_score.total` descending, (5) done for now. Routing for each option lives inline in this SKILL.md, never in `references/` (per the `post-menu-routing-belongs-inline` learning — keep routing discoverable in the loaded skill, not in a file the loader may not pick up).

## VOICE CONTRACT

These rules apply to every `/meta-top` output regardless of region:

- **Badge first.** Line 1 is the badge. No blank lines before it. No preamble.
- **Show, don't summarize, the citations.** Every claim with a sourced fact carries inline `[name](url)`. Sub-bullet for the strongest citation; secondary sources in same citation cluster as `[src1](url1), [src2](url2)`.
- **Currency stays local.** A price point of `500 INR` writes as `₹500`; never `~$6`. If a curated source quotes USD for a non-US region, write the local figure next to a USD annotation in parens (e.g., `₹500 (~$6)`); never lead with USD outside US.
- **Regulatory notes are unmissable.** Put the region's regulatory body and one sentence of what they enforce as a callout blockquote under Section (a). Do not bury it in a paragraph.
- **No vendor endorsements.** The skill surfaces *categories*, *categories*, and *positioning gaps*. It does not name specific brands or creators in the Option B recommendation block (Section f). Naming a specific brand in Sections (b)–(e) is fine when the live research sources it; Section (f) reframes it as `category + angle, not brand + clone`.
- **Disclose uncertainty.** Thin-data regions (UAE, sometimes Canada) carry a `data_quality_note` rather than fabricated benchmarks. The Option B brief must contain at least one pricing tier labeled `pricing_tier_source: observed`; otherwise show `category-pricing-research-required` notice and skip the brief.
- **Per-category winning-product rubric.** Every category in Section (b) renders inline as `- {category-name} · {price-range} · Score: {X}/14 — {band} · [longevity {a}, variants {b}, cross_country {c}, engagement {d}, marketplace {e}, pain_signal {f}]`. The X/14 total is `winning_score.total` from the digest; the band is `strong_bet` (9+), `promising` (6–8), or `skip` (<6). When the sub-agent emits `confidence: low` for one or more signals, append `(confidence: low)` after the breakdown so the user sees evidence depth.
- **Format compliance is visible.** Ad-copy templates in Option B show the format constraints inline (FB primary text ≤125 chars, headline ≤40 chars, IG Reels 9:16 vertical, WA status 24h ephemeral) so the user sees the limits when they reach for the template.
- **No raw URLs, ever.** A URL only appears wrapped in `[name](url)` markdown. Stand-alone URLs in plain text are a defect.

## Reliability: source ladder (v1.1+)

When the host's WebSearch tool is unavailable or returns empty payloads, meta-top does NOT fail outright. The sub-agent walks a transparent 4-tier source ladder. Each tier is fall-through; the next tier only fires when the previous returned < 5 sources (US/IN) or < 3 sources (others).

1. **Host-native WebSearch** — primary tier.
2. **Keyless DDG/SearXNG** — `scripts/keyless_search.py "QUERY" --count 5`. Stdlib-only, no API keys, no recurring cost. Mirrors last30days's `web_search_keyless.py` pattern.
3. **Curated `top_brands`** — direct WebFetch to each brand-domain URL in `references/regions/<region>.yaml`'s `top_brands` list. Cap at 4 fetches; skip any URL that 403s/404s.
4. **Curated anchors only** — final fallback. Brief still ships; `data_quality_note` flags the limitation transparently.

When tier 2 or 3 contributes any source, `partial_research: true` and the `data_quality_note` records which tier filled the gap (e.g., `"Ladder tier 2 contributed 4 sources after WebSearch returned 0."`).

This was added in v1.1 after the v1 smoke-test surfaced WebSearch's empty-payload failure mode (2-of-3 sub-agent runs hit it; tier 2 closed the gap via WebFetch fallback; tier 3 is the same fix routed through a stable Python entry point).

## Step 0: Pre-Flight

Mandatory before dispatching the sub-agent.

1. **Region validation.** Match `<region>` argument against the v1 list: `in`, `us`, `ca`, `uk`, `au`, `ae`. Match is case-insensitive; normalize to the v1 code. If no match, **stop** and emit the region-not-in-v1 response (see Pre-Flight Failure Modes).
2. **Optional flags.** Parse `--category=<name>` (narrows the brief to one top category by name) and `--emit=html` (writes a self-contained HTML brief to `<root>/meta-top-reports/<region>-<YYYY-MM-DD>.html` instead of chat-only). Unknown flags log a one-line FYI in the output footer and are otherwise ignored.
3. **Region mismatch detection.** If the invocation passes a region code that, after normalization, is not in the v1 list, surface the region-not-in-v1 response. If a `--category=<name>` does not appear in the live research's `top_categories` for that region, surface a FYI: `Category "<name>" not in this region's top list — surfacing as cross-category note.`
4. **Objective-vs-format check.** If a region config declares a category with a regulatory restriction (e.g., UAE financial products require Arabic landing pages, US healthcare requires HIPAA-aware copy), surface this in the pre-flight footer so Section (a) can carry it forward.
5. **Repository root resolution.** Resolve `<root>` only if `--emit=html` was passed; otherwise skip. Read `docs_root` from `<repo-root>/.compound-engineering/config.yaml`; if unset, `<root>` is `docs`. Validate: real, symlink-resolved path inside the repo, not the repo root, not under `.git/`.
6. **Sub-agent precondition.** Confirm `references/regions/<region>.yaml` exists. If not, surface a structural error and stop — never fabricate region anchors.

## Step 0.5: Per-Region Resolved Block

This block sits *under* the badge and *above* Section (a) — it tells the reader at a glance what anchors the rest of the report rests on. Pull `region_code`, `display_name`, `currency`, `currency_symbol`, `languages`, `regulatory_body`, `prohibited_categories`, `format_constraints`, `top_categories` from `references/regions/<region>.yaml`. The block looks like:

```
## Resolved

- Region: {display_name} ({region_code})
- Currency: {currency_symbol} {currency}  •  Languages: {languages joined with `, `}
- Regulatory: {regulatory_body.name} — {regulatory_body.one_line_summary} ([{regulatory_body.short}]({regulatory_body.url}))
- Prohibited categories (filtered from live research): {prohibited_categories as comma-joined list}
- Ad formats: FB primary text ≤125 chars, headline ≤40 chars • IG Reels 9:16 vertical, ≤15 s • WA Status 24h ephemeral • verified against Meta docs {format_constraints.last_verified_against_meta_docs}
- Top evergreen categories (seeds for live research): {top_categories — name + positioning_note}
- Last curated review: {last_reviewed}
```

The regulatory body's one-line summary must be the rule of thumb the user needs to remember (e.g., ASCI: "Truthful and non-misleading ads; substantiated claims for health, finance, education").

## Step 1: Dispatch Sub-Agent

Dispatch the curated-region-aware research primitive. Use the platform's Agent tool with sub-agent delegation.

Dispatch the agent at `references/agents/meta-top-researcher.md` (loaded via the Skill tool: `Skill("meta-top-researcher")` if available, otherwise pass `READ` instructions). The agent reads the region's curated YAML anchors and runs live research.

**Pass only the path**, not the YAML content. Per `pass-paths-not-content-to-subagents` learning: orchestrator hands the sub-agent `<absolute path to skills/meta-top/references/regions/<region>.yaml>`; sub-agent reads what it needs.

The agent returns a structured JSON digest (schema lives in `references/agents/meta-top-researcher.md`).

## Step 2: Present Six-Section Synthesis

Render the JSON digest into the canonical six-section template, preserving the badge and Resolved block already emitted. Region-specific anchor rules:

1. **Market snapshot.** Region size, Meta share of digital ad spend, growth direction (last 12 months), regulatory headline. Cite ≥2 sources for non-trivial claims.
2. **Top 5–7 product categories with local-currency pricing.** Each category carries: name, ≥2 cited pricing examples from observed live sources (in local currency), the positioning note from the curated config (if live research concurs) or live-replacement positioning, evidence URLs. Curated-vs-live conflict resolution: live research is authoritative; curated `top_categories` are seeds that get **replaced** when live entries have ≥2 cited sources. Replacements surface in `data_quality_note` under Section (b). **Per-category winning-product rubric (v1.3):** when the digest's `top_categories[]` entry carries `winning_signals` + `winning_score`, render each category line as `- {name} · {currency}{price-range} · Score: {X}/14 — {band} · [longevity {a}, variants {b}, cross_country {c}, engagement {d}, marketplace {e}, pain_signal {f}]` where `{X}` = `winning_score.total` (0–14), `{band}` = `strong_bet` (9+) / `promising` (6–8) / `skip` (<6), and the six sub-scores are `winning_signals.{signal}.sub_score`. If any signal has `confidence: low`, append `(confidence: low)` to the line.
3. **Winning ad creative patterns.** Hook type (curiosity / problem-solution / before-after / testimonial / UGC / offer-stack), format (FB primary text + headline combo / IG Reels 9:16 vertical / carousel / WA Status 24h ephemeral / collection), where currently running. Cite ≥3 sources for patterns.
4. **Specific product examples currently running.** Brand or product name, observed ad-creative angle, observed price point (in local currency), source URL. ≥3 examples; thin-data regions allow ≥2 with a `data_quality_note`.
4a. **Underground signals observed (v1.3, qualitative callout).** When the digest's `underground_signals[]` is non-empty, render a single blockquote titled `Underground signals observed` immediately under Section (d). Each entry is one bullet: `- {kind}: {observation} ([source]({url}))`. Kinds: `scarcity_working` (sold-out → back-again pattern), `refund_policy_questions` (high purchase-intent in comments), `specificity` ("made ₹X in Y days" specific numbers), `creator_collab_to_paid` (organic reshared as ad), `lookalike_1pct_hint` (1% lookalike audience hint). Empty `underground_signals[]` → omit the blockquote entirely; never emit an empty placeholder.
5. **Meta ad cost benchmarks.** CPM range, CPC range, CPV range (where applicable), CTR range — each in local currency, each carrying `evidence_url_count`. When a benchmark cannot be grounded in ≥2 cited sources, return the literal string `"Insufficient public data — refer to Meta Ad Library for live benchmarks"` rather than synthesizing a range. The orchestrator surfaces `[n sources]` next to each value.
6. **Option B actionable brief.** This is the load-bearing output — see Step 3.

## Step 3: Option B Actionable Brief

The Option B section is **structured reference material**, not chat synthesis. Render this section with `##` and `###` headers; do not flatten to prose. The section is titled:

`## f. Option B: Recommended positioning for YOUR original product`

Then inside the brief:

### Pricing tiers (in {currency_symbol})

Three levels in local currency, each with a positioning hint:

- **Entry** — `{currency_symbol}{X}` — `{one-line positioning hint}`
- **Mid** — `{currency_symbol}{X}` — `{one-line positioning hint}`
- **Premium** — `{currency_symbol}{X}` — `{one-line positioning hint}`

At least one tier must come from observed live research (`pricing_tier_source: observed`). If no tier clears the bar, show:

`> category-pricing-research-required — at least one observed pricing example is required before the brief ships. Run \`/meta-top <region> --category=<name>\` after manually observing pricing for the target category.`

The three tiers ladder from "loss-leader checkout" → "core offer" → "anchor / upsell". Localize the positioning hint per region.

### Creative angles (2–3 distinct hooks)

Two to three positioning hooks derived from the live research. Examples (region-specific, not generic):

- Angle 1: speed of result (works in India where UPI-friction makes time-to-first-payment a conversion lever).
- Angle 2: certification / credential (works in UAE where professional upskilling ads carry trust weight).
- Angle 3: community / network effect (works in US where creator-led offers lean on belonging).

Each angle carries a one-paragraph framing + ≥1 cited source from the live research.

### Ad-copy templates (Meta-format-compliant)

Templates with constraints shown inline so the user sees the limits:

**Facebook primary text** (≤125 chars):

```
Hook (≤90 chars): {hooks the reader with the angle}
Body (≤35 chars):  {closes with the offer}
Headline (≤40 chars): {CTA + value}
```

**Instagram Reels 9:16 vertical script** (≤15 s, vertical):

```
0–3 s:  Pattern interrupt — {visual hook}
3–8 s:  Problem + tease
8–13 s: Proof point + CTA
13–15 s: End card
```

**WhatsApp Status 24h ephemeral copy** (≤700 chars total, 4–6 frames):

```
Frame 1: Visual hook
Frame 2: Problem statement
Frame 3: Proof / authority
Frame 4: Offer + CTA
Frame 5: Scarcity / urgency
Frame 6: Send-to-CTA
```

### Trust + ethics one-liner (always present)

Always rendered as a blockquote immediately before the post-menu:

> **Category design, not content cloning.** Find a proven category, identify a positioning gap, create YOUR original product, position with a USP, test small-budget Meta ads, scale what works.

## Step 4: Post-Menu Routing (inline)

After Option B, present a numbered menu via the platform's blocking question tool (`AskUserQuestion` in Claude Code). Five options:

1. **Drill into a category** — user supplies a category name; orchestrator re-dispatches the sub-agent with `--category=<name>`. Use `Skill("meta-top", "<region> --category=<name>")` or re-invoke via the Agent tool with a narrowed dispatch payload.
2. **Save HTML brief** — produces a self-contained `<root>/meta-top-reports/<region>-<YYYY-MM-DD>.html` document mirroring the chat output (per `--emit=html` flow; shares renderer invariants with last30days HTML brief).
3. **Export creative pack** — writes a paste-ready Markdown block of the Option B brief (pricing tiers + creative angles + ad-copy templates) to chat so the user can paste directly into their authoring tool.
4. **Winning-product dashboard (v1.3)** — re-render section-(b) categories as a Markdown table sorted by `winning_score.total` descending. Columns: `Score | Band | Category | Top signal | Sources`. Top signal = the `winning_signals{}.sub_score` with the highest value (ties broken by sub-key declaration order). Sources = count of unique URLs across `winning_signals.*.evidence_urls`. Inline render in chat, no sub-agent dispatch; reuse the digest already in scope.
5. **Done for now** — ends the session with no further action.

Routing for each option lives inline in this SKILL.md — never in `references/` (the `post-menu-routing-belongs-inline` learning: routing placed in a `references/` file is not discoverable by the platform's blocking question tool). If `AskUserQuestion` errors or is unavailable, fall back to a numbered list in chat with the same five options.

## Pre-Flight Failure Modes

### Region not in v1

Stop before dispatch and emit:

```
📊 meta-top v{X} · region: {arg} · {YYYY-MM-DD}

Region "{arg}" is not in the v1 supported list.

v1 regions: india, us, ca, uk, au, ae.

For regions outside v1, try:
- `/last30days <region>` — time-windowed cross-source research, region-agnostic.
- File an upstream issue requesting v2 support (link to docs/guides/meta-top.md once shipped).

Stopping without dispatch.
```

### Brand-collision detection

When the same region + category combination has been called in the last 3 invocations (lightweight dedupe against chat history; if no record exists, skip silently), surface:

> **Heads up** — `/meta-top <region> --category=<name>` was last called {N} invocations ago. Pricing may have shifted. Live research will still run.

### Region-mismatch detection

If `--category=<name>` parses but the category name does not appear in the live research's `top_categories` for that region, surface as a one-line FYI in the footer.

### Objective-vs-format-mismatch detection

If a region's `format_constraints` declare, e.g., that financial products in UAE require Arabic landing pages or US healthcare requires HIPAA-aware copy, surface as a footer blockquote so the user sees it before launching.

## Security and Trust Disclosure

- **Read-only public sources.** Sub-agent uses WebSearch and WebFetch against public Meta Ad Library URLs, regional regulatory bodies, and creator case studies. No Meta Business Manager API calls in v1 (no auth required, no business verification gating).
- **No PII harvesting.** No user emails, account IDs, or message content in saved reports.
- **Url hijacking disclosure.** Cited URLs were verified at research time but may be hijacked, expired, or removed subsequently; users should verify before clicking. Surface this as `data_quality_note: cited_urls_verified_at_research_time_may_have_drifted`.
- **Trust + ethics boundary.** The skill surfaces categories, positioning gaps, and pricing benchmarks. It does NOT recommend cloning specific creator content. The Option B brief is category-level, not brand-level. White-label / franchise / MLM-style digital-product businesses are surfaced as `prohibited_categories` per region config and filtered from live research.
- **v1 ceiling.** Latency budget ≤60 s for a single-region invocation. Longer acceptable for thin-data regions if a `data_quality_note` explains the delay.

## What this skill does not do

To prevent scope creep:

- **No bundled Python script** in v1's main path. All live-data work happens inside the sub-agent via WebSearch/WebFetch. **v1.1 lifts this rule scoped to a floor-tier keyless DDG fallback only** — `scripts/lib/web_search_keyless.py` + `scripts/keyless_search.py` mirror last30days's `web_search_keyless.py` pattern (stdlib-only, no API keys, no recurring cost). The sub-agent uses it as tier 2 of the source ladder, never as a Python replacement for the host's WebSearch. Broader paid-search Python fallbacks (Brave / Serper / SerpAPI / Exa) remain out of scope until v1.5+.
- **No `--last=N`** time-window flag. The skill is a snapshot, not a trend.
- **No `--category=<name>` overlap with `--emit=html`** is allowed; both flags are orthogonal.
- **No multi-language output** in v1. English only.
- **No saving reports to `docs/meta-top-reports/` per run** unless `--emit=html` is passed. v1 default is chat-only.
- **No A/B testing of Meta ad creative** — that's a Meta platform feature, not this skill's job.
- **No historical trend tracking across runs** — snapshot semantics.
