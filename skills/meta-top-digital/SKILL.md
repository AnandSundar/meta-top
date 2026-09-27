---
name: meta-top-digital
description: "Region-aware deep-research report on top-selling digital template/download products (Notion templates, prompt packs, spreadsheets, design assets, ebook bundles, printables) being advertised on Meta (Facebook, Instagram, WhatsApp Business) for a specific region. Six regions in v1: india, us, ca, uk, au, ae. India is the v1 anchor; the other five regions ship via the U5 mirror unit. Strict digital-only scope — courses, cohort programs, SaaS subscriptions, paid memberships, and physical goods are filtered out under each region's `prohibited_categories_digital`. Optionally narrows by product category and produces an Option B actionable brief (pricing tiers in ₹/$/CAD/£/AUD/AED, creative angles, Meta-format-compliant ad-copy templates). Use when asked for top-selling digital templates/downloads on Meta, what Notion-template or prompt-pack to launch, or what CPM/CPC to budget on Meta for digital downloads in a region."
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

# Meta Top Digital — Region-Aware Digital Product Deep-Research on Meta

**Note: The current year is 2026.** Use this when pricing examples, ad-creative patterns, and regulatory notes touch dates or recency claims.

`meta-top-digital` is a region-aware deep-research skill — the **digital-only sibling** of `meta-top` v1.1 — that produces a structured six-section report on top-selling digital template / download / printable products being advertised on Meta (Facebook, Instagram, WhatsApp Business) for one of six v1 regions (India, US, Canada, UK, Australia, UAE), plus an Option B actionable brief (₹/$/CAD/£/AUD/AED pricing tiers, creative angles, Meta-format-compliant ad-copy templates).

In v1, **India is the only region with a verified region YAML**; the other five regions (`us`, `ca`, `uk`, `au`, `ae`) ship via the U5 mirror unit in the same plan. Until the mirror lands, those regions return an explicit `region-not-yet-shipped` notice — never a silent fallback to the India YAML. See **Pre-Flight > Region not yet shipped** below.

Trust + ethics frame baked in: category design, not content cloning. Cloning of specific creator content is **never** the recommendation — the skill surfaces winning categories and positioning gaps so the user can build their *original* digital product with a sharper angle. Strict scope: **no courses, no cohort programs, no SaaS subscriptions, no paid memberships, no physical goods.** Live research matching any of these is filtered out under each region's `prohibited_categories_digital` and surfaced in `filtered_patterns`.

## SKILL CONTRACT (do not improvise)

A `/meta-top-digital <region>` invocation is complete when:

1. Line 1 of the output is the badge: `📊 meta-top-digital v{X} · region: {region} · {YYYY-MM-DD}`. `{X}` is this skill's version (currently `v1.2`); bump it intentionally when shipping breaking changes, never auto-increment per invocation.
2. The six canonical sections are present in this order: (a) Market snapshot, (b) Top 5–7 **digital categories** with local-currency pricing, (c) Winning ad creative patterns, (d) Specific product examples, (e) Meta ad cost benchmarks (CPM/CPC/CPV in the region's local currency), (f) Option B actionable brief.
3. Every price reference is in the region's local currency (₹ / $ / CAD / £ / AUD / AED). USD is permitted as a secondary annotation only when ground-truth sources report USD (rare); never silently convert.
4. Every citation is inline `[name](url)` markdown. **No raw URLs. No trailing Sources block. No broken empty `[]()` links.** URLs use `http://` or `https://`; `javascript:`, `data:`, `file:` are rejected.
5. Regulatory notes for the region are surfaced explicitly (never silently dropped). At least one para or blockquote per output cites the regulatory body (ASCI for India, FTC for US, ASA for UK, AANA for AU, Ad Standards + CRTC for CA, NMC + TRA for UAE).
6. A trust + ethics one-liner appears under Option B: **"Category design, not content cloning. Find a proven category, identify a positioning gap, create YOUR original product, position with a USP, test small-budget Meta ads, scale what works."**
7. `data_freshness_note` and `data_quality_note` appear under Section (b) when the live research surfaces thin data or rate-limit / partial-research conditions. Honest caveats are load-bearing output, not optional polish.
8. After Option B, a post-menu is presented inline via the platform's blocking question tool with these four options: (1) drill into a specific category with a follow-up `/meta-top-digital <region> --category=<name>`, (2) save a self-contained HTML brief via `--emit=html`, (3) export the Option B creative pack as a paste-ready Markdown block, (4) done for now. Routing for each option lives inline in this SKILL.md, never in `references/` (per the `post-menu-routing-belongs-inline` learning — keep routing discoverable in the loaded skill, not in a file the loader may not pick up).

## VOICE CONTRACT

These rules apply to every `/meta-top-digital` output regardless of region:

- **Badge first.** Line 1 is the badge. No blank lines before it. No preamble.
- **Show, don't summarize, the citations.** Every claim with a sourced fact carries inline `[name](url)`. Sub-bullet for the strongest citation; secondary sources in same citation cluster as `[src1](url1), [src2](url2)`.
- **Currency stays local.** A price point of `500 INR` writes as `₹500`; never `~$6`. If a curated source quotes USD for a non-US region, write the local figure next to a USD annotation in parens (e.g., `₹500 (~$6)`); never lead with USD outside US.
- **Regulatory notes are unmissable.** Put the region's regulatory body and one sentence of what they enforce as a callout blockquote under Section (a). Do not bury it in a paragraph.
- **No vendor endorsements.** The skill surfaces *digital categories* and *positioning gaps*. It does not name specific creators in the Option B recommendation block (Section f). Naming a specific creator or template pack in Sections (b)–(e) is fine when the live research sources it; Section (f) reframes it as `category + angle, not clone + steal`.
- **Disclose uncertainty.** Thin-data regions (UAE, sometimes Canada) carry a `data_quality_note` rather than fabricated benchmarks. The Option B brief must contain at least one pricing tier labeled `pricing_tier_source: observed`; otherwise show `category-pricing-research-required` notice (see Hard-Block below) and skip the brief.
- **Format compliance is visible.** Ad-copy templates in Option B show the format constraints inline (FB primary text ≤125 chars, headline ≤40 chars, IG Reels 9:16 vertical, WA status 24h ephemeral) so the user sees the limits when they reach for the template.
- **No raw URLs, ever.** A URL only appears wrapped in `[name](url)` markdown. Stand-alone URLs in plain text are a defect.

### Hard-Block: brief does not ship without an observed pricing tier

R10 (from the plan's requirements) is a hard-block: if no pricing tier in the live research carries `pricing_tier_source: observed`, the brief does not ship. Output the blockquote:

> **⚠️ category-pricing-research-required** — at least one observed pricing example is required before the brief ships. Run `/meta-top-digital <region> --category=<name>` after manually observing pricing for the target category (one paid marketplace URL is enough). **If the host environment has the playwright MCP server configured, the next invocation will auto-attempt the tier-4 browser fallback and may clear the hard-block without manual intervention** — verify the MCP is available before relying on this. When all ladders (including tier 4) return zero observed prices, do **not** promote the seed tier anchors (₹199/₹599/₹1,999 for India; equivalent local-currency anchors per region) as concrete tiers — surface them under Section (b) with a `[unverified starting points, not observed]` callout and stop.

This is fail-closed: a brief built on unobserved seed prices is the failure mode this skill explicitly guards against.

## Reliability: source ladder (v1.2+, mirror of meta-top v1.1)

When the host's WebSearch tool is unavailable or returns empty payloads, meta-top-digital does NOT fail outright. The sub-agent walks a transparent 5-tier source ladder. Each tier is fall-through; the next tier only fires when the previous returned **≤5 sources** (US/IN) or **< 3 sources** (others). The ladder is the **same** floor meta-top v1.1 uses — `scripts/keyless_search.py` is copied verbatim from `skills/meta-top/scripts/`, and any future divergence lives upstream, never here.

1. **Host-native WebSearch** — primary tier.
2. **Keyless DDG/SearXNG** — `scripts/keyless_search.py "QUERY" --count 5`. Stdlib-only, no API keys, no recurring cost. Mirrors last30days's `web_search_keyless.py` pattern.
3. **Curated `digital_marketplaces`** — direct WebFetch to each marketplace-domain URL in `references/regions/<region>.yaml`'s `digital_marketplaces` list. Cap at 4 fetches; skip any URL that 403s/404s. Marketplace URLs are stable catalog/index pages (gumroad.com/discover, instamojo.com/featured, notion.so/marketplace, creativemarket.com, canva.com/creators), so they survive subdomain migrations better than individual creator-store URLs.
4. **Playwright browser fallback** *(v1.2+, 2026-09-27)* — when tier 3 returns 403/404 on **≥2 marketplace URLs** OR `pricing_examples` is empty across all `top_categories` after tier 3, fall through to a real browser via the **playwright MCP server** (`mcp__plugin_playwright_playwright__browser_*`). Use `browser_navigate` + `browser_snapshot` (a11y-tree) to render JS-driven marketplace surfaces (Canva Creators, dynamic Gumroad search, Instamojo storefront pages) and extract per-product INR prices that WebFetch cannot see. Cap at **≤2 browser navigations per invocation** to respect the latency budget. **Skip this tier entirely if the playwright MCP server is not configured in the host environment** — fall through to tier 5. This tier is **browser automation, not a Python fallback**; no `pip install` of the `playwright` Python package required.
5. **Curated anchors only** — final fallback. Brief still ships; `data_quality_note` flags the limitation transparently.

When tier 2, 3, or 4 contributes any source, `partial_research: true` and the `data_quality_note` records which tier filled the gap (e.g., `"Ladder tier 4 (Playwright) contributed 2 sources after WebFetch returned 403 on Canva and Instamojo."`).

Scope ceiling (matching meta-top v1.1 line 85 — do not regress to off-by-one): ≤8 total sources across all tiers; ≤20 total fetch calls across the whole invocation (seed queries + tier 3 WebFetch + tier 4 Playwright navigations). Playwright navigations count toward the 20-call ceiling, not separately.

## Step 0: Pre-Flight

Mandatory before dispatching the sub-agent.

1. **Region validation.** Match `<region>` argument against the v1 list: `in`, `us`, `ca`, `uk`, `au`, `ae`. Match is case-insensitive; normalize to the v1 code. If no match, **stop** and emit the region-not-in-v1 response (see Pre-Flight Failure Modes).
2. **Region-mirror check.** If the region is **in the v1 list** but its YAML is missing from `skills/meta-top-digital/references/regions/<region>.yaml` (only India is shipped in v1; US, CA, UK, AU, AE arrive in the U5 mirror unit), emit the region-not-yet-shipped notice below and stop. Never silently fall back to the India YAML.
3. **Optional flags.** Parse `--category=<name>` (narrows the brief to one digital category by name) and `--emit=html` (writes a self-contained HTML brief to `<root>/meta-top-reports/<region>-<YYYY-MM-DD>.html` instead of chat-only). Unknown flags log a one-line FYI in the output footer and are otherwise ignored.
4. **Region mismatch detection.** If `--category=<name>` does not appear in the live research's `digital_categories` for that region, surface a FYI: `Category "<name>" not in this region's digital-only top list — surfacing as cross-category note.`
5. **Objective-vs-format check.** If a region config declares a category with a regulatory restriction (e.g., UAE financial products require Arabic landing pages, US healthcare requires HIPAA-aware copy), surface this in the pre-flight footer so Section (a) can carry it forward.
6. **Repository root resolution.** Resolve `<root>` only if `--emit=html` was passed; otherwise skip. Read `docs_root` from `<repo-root>/.compound-engineering/config.yaml`; if unset, `<root>` is `docs`. Validate: real, symlink-resolved path inside the repo, not the repo root, not under `.git/`.
7. **Sub-agent precondition.** Confirm `references/regions/<region>.yaml` exists. If not, surface a structural error and stop — never fabricate region anchors.

## Step 0.5: Per-Region Resolved Block

This block sits *under* the badge and *above* Section (a) — it tells the reader at a glance what anchors the rest of the report rests on. Pull `region_code`, `display_name`, `currency`, `currency_symbol`, `languages`, `regulatory_body`, `prohibited_categories_digital`, `format_constraints`, `digital_categories`, `digital_marketplaces` from `references/regions/<region>.yaml`. The block looks like:

```
## Resolved

- Region: {display_name} ({region_code})
- Currency: {currency_symbol} {currency}  •  Languages: {languages joined with `, `}
- Regulatory: {regulatory_body.name} — {regulatory_body.one_line_summary} ([{regulatory_body.short}]({regulatory_body.url}))
- Prohibited categories (digital-only scope, filtered from live research): {prohibited_categories_digital as comma-joined list}
- Ad formats: FB primary text ≤125 chars, headline ≤40 chars • IG Reels 9:16 vertical, ≤15 s • WA Status 24h ephemeral • verified against Meta docs {format_constraints.last_verified_against_meta_docs}
- Top evergreen digital categories (seeds for live research): {digital_categories — name + positioning_note}
- Marketplace anchors (tier-3 ladder fetch): {digital_marketplaces — name + url, 5–8 entries}
- Last curated review: {last_reviewed}
```

The regulatory body's one-line summary must be the rule of thumb the user needs to remember (e.g., ASCI: "Truthful and non-misleading ads; substantiated claims for health, finance, education").

## Step 1: Dispatch Sub-Agent

Dispatch the curated-region-aware research primitive. Use the platform's Agent tool with sub-agent delegation.

Dispatch the agent at `references/agents/meta-top-digital-researcher.md` (loaded via the Skill tool: `Skill("meta-top-digital-researcher")` if available, otherwise pass `READ` instructions). The agent reads the region's curated YAML anchors and runs live research.

**Pass only the path**, not the YAML content. Per `pass-paths-not-content-to-subagents` learning: orchestrator hands the sub-agent `<absolute path to skills/meta-top-digital/references/regions/<region>.yaml>`; sub-agent reads what it needs.

The agent returns a structured JSON digest (schema lives in `references/agents/meta-top-digital-researcher.md`).

## Step 2: Present Six-Section Synthesis

Render the JSON digest into the canonical six-section template, preserving the badge and Resolved block already emitted. Region-specific anchor rules:

1. **Market snapshot.** Region size, Meta share of digital ad spend (focused on the digital-template / download vertical), growth direction (last 12 months), regulatory headline. Cite ≥2 sources for non-trivial claims.
2. **Top 5–7 digital categories with local-currency pricing.** Each category carries: name, ≥1 cited observed pricing example from a live marketplace landing page (in local currency), the positioning note from the curated config (if live research concurs) or live-replacement positioning, evidence URLs. Curated-vs-live conflict resolution: live research is authoritative; curated `digital_categories` are seeds that get **replaced** when live entries have ≥2 cited sources. Replacements surface in `data_quality_note` under Section (b). **Hard-block reminder:** if no observed pricing example clears the bar across all categories, the Option B brief does not ship — see Hard-Block above.
3. **Winning ad creative patterns** for digital templates / downloads. Hook types include: UGC testimonial of a digital product (mock-up carousel showing the template in Notion / Sheets / Canva), before-after prompt-pack demo (split-screen: blank prompt → populated AI output), instant-download carousel (hero shot of the product, then 3-4 frames previewing structure), and offer-stack (e.g., "Notion template + free prompt pack + bonus checklist"). Formats: FB primary text + headline combo, IG Reels 9:16 vertical (15-second walkthrough), carousel (4-6 frames previewing template structure), WA Status 24h ephemeral (URL-only drops with screenshot teaser). Cite ≥3 sources for patterns.
4. **Specific product examples currently running.** **Digital product** name (template pack / prompt pack / spreadsheet / design asset / ebook bundle / printable), observed ad-creative angle, observed price point (in local currency), source URL. **Strict filter:** any course, cohort program, SaaS subscription, paid membership, or physical-good product is filtered out under `prohibited_categories_digital` and surfaced in `filtered_patterns` — never in this section. ≥3 examples; thin-data regions allow ≥2 with a `data_quality_note`.
5. **Meta ad cost benchmarks.** CPM range, CPC range, CPV range (where applicable), CTR range — each in local currency, each carrying `evidence_url_count`. When a benchmark cannot be grounded in ≥2 cited sources, return the literal string `"Insufficient public data — refer to Meta Ad Library for live benchmarks"` rather than synthesizing a range. The orchestrator surfaces `[n sources]` next to each value.
6. **Option B actionable brief.** This is the load-bearing output — see Step 3.

## Step 3: Option B Actionable Brief

The Option B section is **structured reference material**, not chat synthesis. Render this section with `##` and `###` headers; do not flatten to prose. The section is titled:

`## f. Option B: Recommended positioning for YOUR original digital product`

Then inside the brief:

### Pricing tiers (in {currency_symbol})

Three levels in local currency, each with a positioning hint. Seed anchors for India (replace with region-specific seeds when the mirror YAMLs land in U5):

- **Entry** — `₹199` — instant-download loss-leader (single Notion template, single prompt pack). Hook on speed-of-result: "Download → use in 5 minutes."
- **Mid** — `₹599` — core offer (Notion template bundle, full prompt pack with variations, multi-page Canva kit). The "shipping tier."
- **Premium** — `₹1,999` — anchor / upsell (Notion life-OS system, GPT-prompt operating system, design-asset vault with commercial license). The "perceived-value tier."

At least one tier must come from observed live research (`pricing_tier_source: observed`); the seed anchors are **unverified starting points**, not observed, until a marketplace URL grounds them. If no tier clears the bar, show the Hard-Block callout (above) and do not ship the brief.

The three tiers ladder from "loss-leader checkout" → "core offer" → "anchor / upsell". For non-IN regions, replace ₹ with the region's local currency and adjust the positioning hints; the tier ladder (Entry / Mid / Premium) stays the same shape.

### Creative angles (2–3 distinct hooks for digital templates / downloads)

Two to three positioning hooks derived from the live research, oriented to digital downloads — never to courses or cohorts:

- Angle 1: instant download / speed of result (works in India where UPI-friction makes time-to-first-payment a conversion lever; digital products turn this into "download in 60 seconds, use tonight").
- Angle 2: structured-template promise (positions against the "blank-canvas problem"; "Stop starting from scratch — this Notion template is the second brain already wired.").
- Angle 3: life-OS / workflow-fit (positions the product as a system, not a one-shot; "Notion-based, lives inside your existing workspace.")

Each angle carries a one-paragraph framing + ≥1 cited source from the live research.

### Ad-copy templates (Meta-format-compliant)

Templates with constraints shown inline so the user sees the limits:

**Facebook primary text** (≤125 chars):

```
Hook (≤90 chars): {hooks the reader with the angle — "I built the Notion system so you don't have to."}
Body (≤35 chars):  {closes with the offer — "₹599. Instant download."}
Headline (≤40 chars): {CTA + value — "Get the template — Notion + Sheets bundle"}
```

**Instagram Reels 9:16 vertical script** (≤15 s, vertical):

```
0–3 s:  Pattern interrupt — {template mock-up scroll, "before/after" of blank → populated}
3–8 s:  Problem + tease — "stop starting from scratch, this template does step 1 for you"
8–13 s: Proof point + CTA — "₹599, instant download, lifetime updates"
13–15 s: End card — name + URL
```

**WhatsApp Status 24h ephemeral copy** (≤700 chars total, 4–6 frames):

```
Frame 1: Visual hook — template preview
Frame 2: Problem statement — "blank canvas, no time"
Frame 3: Proof / authority — preview thumbnail + "I built the system, you use it"
Frame 4: Offer + CTA — "₹599, instant download"
Frame 5: Scarcity / urgency — "lifetime updates included, free revisions this week"
Frame 6: Send-to-CTA — comment / DM / link sticker
```

### Trust + ethics one-liner (always present)

Always rendered as a blockquote immediately before the post-menu:

> **Category design, not content cloning.** Find a proven category, identify a positioning gap, create YOUR original product, position with a USP, test small-budget Meta ads, scale what works.

## Step 4: Post-Menu Routing (inline)

After Option B, present a numbered menu via the platform's blocking question tool (`AskUserQuestion` in Claude Code). Four options:

1. **Drill into a category** — user supplies a category name; orchestrator re-dispatches the sub-agent with `--category=<name>`. Use `Skill("meta-top-digital", "<region> --category=<name>")` or re-invoke via the Agent tool with a narrowed dispatch payload.
2. **Save HTML brief** — produces a self-contained `<root>/meta-top-reports/<region>-<YYYY-MM-DD>.html` document mirroring the chat output (per `--emit=html` flow; shares renderer invariants with last30days HTML brief).
3. **Export creative pack** — writes a paste-ready Markdown block of the Option B brief (pricing tiers + creative angles + ad-copy templates) to chat so the user can paste directly into their authoring tool.
4. **Done for now** — ends the session with no further action.

Routing for each option lives inline in this SKILL.md — never in `references/` (the `post-menu-routing-belongs-inline` learning: routing placed in a `references/` file is not discoverable by the platform's blocking question tool). If `AskUserQuestion` errors or is unavailable, fall back to a numbered list in chat with the same four options.

## Pre-Flight Failure Modes

### Region not in v1

Stop before dispatch and emit:

```
📊 meta-top-digital v{X} · region: {arg} · {YYYY-MM-DD}

Region "{arg}" is not in the v1 supported list.

v1 regions: india, us, ca, uk, au, ae.

For regions outside v1, try:
- `/meta-top <region>` — meta-top's broader Meta-ads research (covers physical D2C, cohorts, SaaS in addition to digital).
- `/last30days <region>` — time-windowed cross-source research, region-agnostic.
- File an upstream issue requesting v2 support (link to docs/guides/meta-top.md once shipped).

Stopping without dispatch.
```

### Region not yet shipped (mirror landed later)

For regions in the v1 list whose YAML is not yet present in `skills/meta-top-digital/references/regions/` (in v1 only India ships; US, CA, UK, AU, AE arrive in the U5 mirror unit), stop and emit:

```
📊 meta-top-digital v{X} · region: {arg} · {YYYY-MM-DD}

Region "{arg}" ({display_name}) is in the v1 region list, but its region
YAML has not shipped yet in this skill. Only India (in) is live in v1;
the other five v1 regions arrive via the U5 mirror unit.

v1 ship status:
  ✓ in (India) — references/regions/in.yaml present
  ⏳ us, ca, uk, au, ae — U5 mirror unit, planned

Workaround for non-IN users:
  1. Use `/meta-top <region>` for the broader Meta-ads brief (covers
     physical D2C + cohorts + SaaS + digital downloads).
  2. Watch the GitHub repo for the U5 mirror release.

Stopping without dispatch.
```

The notice names the v1 ship status and points to `/meta-top` as the immediate workaround — it does **not** silently fall back to the India YAML.

### Brand-collision detection

When the same region + category combination has been called in the last 3 invocations (lightweight dedupe against chat history; if no record exists, skip silently), surface:

> **Heads up** — `/meta-top-digital <region> --category=<name>` was last called {N} invocations ago. Pricing may have shifted. Live research will still run.

### Region-mismatch detection

If `--category=<name>` parses but the category name does not appear in the live research's `digital_categories` for that region, surface as a one-line FYI in the footer.

### Objective-vs-format-mismatch detection

If a region's `format_constraints` declare, e.g., that financial products in UAE require Arabic landing pages or US healthcare requires HIPAA-aware copy, surface as a footer blockquote so the user sees it before launching.

## Security and Trust Disclosure

- **Read-only public sources.** Sub-agent uses WebSearch and WebFetch against public Meta Ad Library URLs, regional regulatory bodies, and public marketplace landing pages (Gumroad India, Instamojo top-sellers, Notion Marketplace, Creative Market, Canva Creators, etc.). No Meta Business Manager API calls in v1 (no auth required, no business verification gating).
- **Digital-only scope gate.** Live research that surfaces a course, cohort program, SaaS subscription, paid membership, or physical-good product is **filtered** under `prohibited_categories_digital` and reported in `filtered_patterns`. The Option B brief is digital-template-only and refuses to recommend cloning such sources.
- **No PII harvesting.** No user emails, account IDs, or message content in saved reports.
- **Url hijacking disclosure.** Cited URLs were verified at research time but may be hijacked, expired, or removed subsequently; users should verify before clicking. Surface this as `data_quality_note: cited_urls_verified_at_research_time_may_have_drifted`.
- **Trust + ethics boundary.** The skill surfaces categories, positioning gaps, and pricing benchmarks. It does NOT recommend cloning specific creator content. The Option B brief is category-level, not creator-level. MLM / network-marketing signals, crypto-token-presale mechanics, get-rich-quick income claims, and any pattern matching `prohibited_categories_digital` are filtered from live research.
- **v1 ceiling.** Latency budget ≤60 s for a single-region invocation. Longer acceptable for thin-data regions if a `data_quality_note` explains the delay.

## What this skill does not do

To prevent scope creep:

- **No courses, cohort programs, SaaS subscriptions, paid communities, or physical goods** in the brief. Live research matching these is filtered out under `prohibited_categories_digital` per region.
- **No bundled Python script** in v1's main path. All live-data work happens inside the sub-agent via WebSearch/WebFetch. **v1.1 lifts this rule scoped to a floor-tier keyless DDG fallback only** — `scripts/lib/web_search_keyless.py` + `scripts/keyless_search.py` mirror meta-top's `web_search_keyless.py` pattern (stdlib-only, no API keys, no recurring cost), copied byte-for-byte from `skills/meta-top/scripts/`. The sub-agent uses it as tier 2 of the source ladder, never as a Python replacement for the host's WebSearch. **Tier 4 (Playwright browser fallback, v1.2+) is browser automation, not a Python fallback** — it uses the playwright MCP server (`mcp__plugin_playwright_playwright__browser_*`) to render JS-driven marketplace surfaces that WebFetch cannot reach. The MCP server must be configured in the host environment; if it is not, tier 4 is skipped and the ladder falls through to curated anchors only. Broader paid-search Python fallbacks (Brave / Serper / SerpAPI / Exa) remain out of scope until v1.5+.
- **No `--last=N`** time-window flag. The skill is a snapshot, not a trend.
- **No `--category=<name>` overlap with `--emit=html`** is allowed; both flags are orthogonal.
- **No multi-language output** in v1. English only.
- **No saving reports to `docs/meta-top-reports/` per run** unless `--emit=html` is passed. v1 default is chat-only.
- **No A/B testing of Meta ad creative** — that's a Meta platform feature, not this skill's job.
- **No historical trend tracking across runs** — snapshot semantics.
- **No creator-level recommendations in Option B.** Specific creators/template packs appear only as observational data in Sections (b)–(e), never as recommendations in (f).
