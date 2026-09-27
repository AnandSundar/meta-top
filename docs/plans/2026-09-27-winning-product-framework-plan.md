---
artifact_contract: ce-unified-plan/v1
product_contract_source: ce-plan-bootstrap
execution: code
title: "Winning-Product Detection Framework"
type: feat
date: 2026-09-27
---

# Winning-Product Detection Framework

## Goal Capsule

Bake a 6-signal winning-product detection rubric into both `meta-top` (v1 → v1.3) and `meta-top-digital` (v1 → v1.3) so that every `/meta-top <region>` and `/meta-top-digital <region>` invocation surfaces, per category, a `X/14` winning-product score alongside the existing local-currency pricing and positioning note. The skill surfaces the intelligence (signals + score); downstream tools consume it. Underground signals (scarcity working, refund-policy comments, "made ₹X" specificity, creator-collab organic-to-paid, 1% lookalike hints) appear as a qualitative callout adjacent to the specific-examples section — never as a 7th scored signal, preserving 14 as the clean rubric ceiling. A 5th post-menu option ("winning-product dashboard") renders the section-(b) categories ranked by score. No new regions, no new tools, no new infrastructure.

### Means (KTD1)

Three-layer architecture, mirrored across both skills:

```
┌──────────────────────────────────────────────────────────────────────┐
│  L1 — Orchestrator (skills/<skill>/SKILL.md)                         │
│    • Badge v1 → v1.3                                                 │
│    • Step 2.2 — render per-category X/14 rubric line in Section (b)  │
│    • Step 2.6 — render underground-signals callout after Section (d) │
│    • Step 4 — 5th post-menu option ("winning-product dashboard")     │
└────────────────────────┬─────────────────────────────────────────────┘
                         │  pass region YAML path (not content)
                         ▼
┌──────────────────────────────────────────────────────────────────────┐
│  L2 — Sub-agent (references/agents/<skill>-researcher.md)            │
│    • New Step 3c — Signal Extraction (6 signals + underground)      │
│    • 4 new canonical WebSearch queries                                │
│    • JSON schema: winning_signals{} + winning_score{} per category   │
└────────────────────────┬─────────────────────────────────────────────┘
                         │  region YAML path only
                         ▼
┌──────────────────────────────────────────────────────────────────────┐
│  L3 — Region anchors (references/regions/<region>.yaml)              │
│    • signal_seeds[] — region-specific search seeds per signal        │
│    • (no new top-level fields; signal_seeds is additive)            │
└──────────────────────────────────────────────────────────────────────┘
```

## Product Contract

### Summary

Both `meta-top` and `meta-top-digital` currently surface *categories* and *pricing*. They do not currently score *winningness*. This plan adds that score. Each category in the live-research JSON digest grows a `winning_signals` object (6 sub-scores, each 0–max per the rubric) and a `winning_score` object (total + band label). The orchestrator renders `Score: X/14 — <band>` inline next to each category in Section (b). Underground signals render as a single qualitative callout after Section (d), citing which specific-examples surface them. The post-menu grows from 4 → 5 options; the new option renders section-(b) categories sorted by `winning_score.total` descending.

### Problem Frame

Meta does not publish a "best-selling list" for digital products. Without a structured rubric, users eyeball pricing and call a winner; with the rubric, the same eyeball call is grounded in six stackable, evidence-backed signals (ad longevity on Meta Ad Library, variant count from one advertiser, cross-country rollout, engagement density, marketplace velocity, demand-side pain). The framework turns a 60-second heuristic into a 30-minute weekly refresh workflow — but only if the signals land inside the skills the user already runs, not in a separate dashboard.

### Requirements

**R1 — Six-signal scoring per category** (governs U1, U2, U9, U10; mirrors to both skills). Each `top_categories[]` entry in the sub-agent's JSON digest carries a `winning_signals` object with six sub-keys, each `{ sub_score: 0|max, evidence_urls: [≥2 URLs preferred, 1 minimum per signal], confidence: high|medium|low }`:

- `longevity` — 0 / 2 / 3 (30+ days → 2; 90+ days → 3)
- `variants` — 0 / 2 / 3 (<3 variants → 0; 5–10 → 2; 20+ → 3)
- `cross_country` — 0 / 1 / 2 (1 country → 0; 2–3 → 1; 5+ → 2)
- `engagement` — 0 / 1 / 2 (low comments → 0; moderate → 1; high buying-intent → 2)
- `marketplace` — 0 / 1 / 2 (flat/declining → 0; stable → 1; rising 50%+ → 2)
- `pain_signal` — 0 / 1 / 2 (few mentions → 0; repeated → 1; "desperate" tone → 2)

Max = 14. Bands: `9+ = strong_bet`, `6–8 = promising`, `<6 = skip`.

**R2 — `winning_score` rollup per category**. Each `top_categories[]` entry carries `winning_score: { total: <0–14>, band: "strong_bet" | "promising" | "skip", computed_at: <YYYY-MM-DD> }`. `total` is the sum of the six sub-scores; `band` is deterministic per the bands above. `computed_at` is the live-research invocation date.

**R3 — Underground-signals callout**. A single blockquote appears under Section (d) (Specific product examples), titled `Underground signals observed` and listing any of these that the live research surfaced: scarcity working ("sold out → back again" pattern), high-purchase-intent comments (refund-policy questions), specificity ("made ₹X in Y days"), creator collab posts being reshared as ads (organic-to-paid), 1% lookalike audience hints. Each surfaced signal carries ≥1 cited URL and a one-line observation. Empty callout text is allowed (omit the section rather than emit empty placeholder) but never fabricate.

**R4 — 5th post-menu option**. The `AskUserQuestion` post-menu grows from 4 → 5 options. New option 5: **Winning-product dashboard** — renders section-(b) categories sorted by `winning_score.total` descending in a Markdown table with `Score | Band | Category | Top signal | Sources`. Routing inline in SKILL.md (per `post-menu-routing-belongs-inline` learning).

**R5 — Badge bump v1 → v1.3**. Both skills' badges change from `📊 meta-top v1 · region: …` / `📊 meta-top-digital v1 · region: …` to `📊 meta-top v1.3 · region: …` / `📊 meta-top-digital v1.3 · region: …`. Justification: SKILL contract item 8 changes (5-option post-menu), Section (b) rendering changes (rubric line), new Section between (d) and (e) (underground callout). Three additive changes justify the minor version bump per the skill's bump-on-breaking-change rule.

**R6 — Cross-skill parity**. Every requirement (R1–R5, R7–R14) ships in *both* `meta-top` and `meta-top-digital`. The digital sibling uses the same rubric shape; the only difference is which sub-agents gather which signals (digital-only signals lean on Gumroad/Etsy/Notion Marketplace rather than broader D2C-marketplace surface — but the JSON keys and band thresholds are identical).

**R7 — Sub-agent JSON schema addition**. `meta-top-researcher.md` and `meta-top-digital-researcher.md` grow a `winning_signals` + `winning_score` field per `top_categories[]` entry. The existing JSON schema (already in both researcher files) is extended; old keys (`name`, `positioning_note`, `pricing_examples`, `evidence_urls`) are unchanged.

**R8 — Four new canonical WebSearch queries per sub-agent**. Sub-agent Step 3 grows from 6 → 10 seed queries. New queries (added after the existing 6 in declaration order, with the digital sibling using digital-marketplace phrasing):

- meta-top: `<region> <category> site:facebook.com/ads/library running since` (longevity)
- meta-top: `<region> <category> advertiser variants count scaling` (variants)
- meta-top: `<region> <category> reddit r/entrepreneur r/saas pain point` (pain-signal)
- meta-top-digital: `<region> <category> Gumroad trending tags rising 2026` (marketplace velocity)
- meta-top-digital: `<region> <category> Etsy movers shakers templates 2026` (marketplace velocity)
- meta-top-digital: `<region> <category> Topmate creators digital products India 2026` (marketplace velocity, IN only)
- meta-top-digital: `<region> <category> Notion Marketplace creator top sellers 2026` (marketplace velocity)

The 4-query budget per category-region pair is enforced via the existing 8-source ceiling — sub-agent already caps at 8 sources total per invocation; new queries join the existing 6 within that ceiling, not on top of it.

**R9 — Region YAML `signal_seeds` field**. Each of the 12 region YAMLs (6 for meta-top + 6 for meta-top-digital) grows a top-level `signal_seeds` object with six keys (one per R1 signal) whose values are region-specific search-query fragments. Example for `in.yaml` (meta-top):

```yaml
signal_seeds:
  longevity: "site:facebook.com/ads/library India {category} active 90 days"
  variants: "{category} India Meta ads variants scaling"
  cross_country: "{category} Meta ads US UK CA AU"
  engagement: "{category} India Meta ad comments buying intent"
  marketplace: "{category} India Gumroad Instamojo Topmate trending"
  pain_signal: "{category} India reddit r/IndianInvestments r/developersIndia pain point"
```

`{category}` is the sub-agent's runtime substitution. `signal_seeds` is additive — existing fields unchanged.

**R10 — No new tools, no new APIs**. The framework uses existing tools only: WebSearch, WebFetch, Meta Ad Library (free, public, no API key), Gumroad/Etsy discover pages (free, public, no API key), Google Trends (free, public, no API key), Reddit search (free, public, no API key). Paid tools (Pipiads / MagicBrief / Foreplay / AdSpy / SEMrush / Ahrefs / SparkToro / Tubular Labs / Sensor Tower) are explicitly out of scope — they are referenced in the data-quality footnote as "optional upgrade path" but never queried by the sub-agent. This preserves the no-Meta-Business-Manager-API rule from both skills.

**R11 — Underground signals are qualitative, not scored**. Per the Phase-0.7 synthesis carry-forward: underground signals (scarcity working, refund-policy comments, "made ₹X" specificity, creator-collab organic-to-paid, 1% lookalike hints) appear as a callout, not as a 7th scored signal. This preserves 14 as the clean rubric ceiling and keeps the band thresholds stable (9+ / 6–8 / <6).

**R12 — `winning_score` is computed by the sub-agent, not the orchestrator**. The sub-agent emits `winning_score.total` and `winning_score.band` in the JSON digest. The orchestrator renders; it does not re-compute. This keeps the score deterministic from the digest (a property downstream tools can rely on).

**R13 — Thin-data regions still emit `winning_score`**. When a region has fewer than 8 sources, the sub-agent still emits a `winning_score` per category, but with lower per-signal `confidence` (set to `low` for signals that could not be evidence-grounded). `winning_score.total` reflects the sum regardless; the orchestrator surfaces `confidence: low` inline. This is fail-soft: missing signals score 0, not fail-closed.

**R14 — No historical tracking of scores across runs**. The score is per-invocation, snapshot-style. This matches the existing `last30days`-style snapshot semantics in both skills. Historical trend tracking is explicitly out of scope (deferred — see Scope Boundaries).

### Key Decisions (carried forward from Phase 0.7)

| Decision | Choice | Rationale | Source | Governs |
|---|---|---|---|---|
| Skill scope | Both skills (`meta-top` + `meta-top-digital`) | Surface winning-product intelligence in both ecosystems; the rubric is vertical-agnostic (digital or broader D2C) | session-settled (user-directed) | R1, R2, R3, R4, R5, R6, R7, R8, R9 |
| Report surface | Per-category rubric `X/14` inline at the category level | Scoring stays visible at the category level; summary-only would hide the rubric shape; dashboard-only would orphan it from the canonical report | session-settled (user-directed) | R1, R2 (orchestrator rendering) |
| Data source | Live research via sub-agent | Signals reflect current Meta activity, not stale anchors; matches existing skill architecture (live research is the source of truth) | session-settled (user-directed) | R1, R7, R8, R13 |
| Underground-signals treatment | Qualitative callout (R3, R11) — not a 7th scored signal | Preserves 14 as the clean rubric ceiling; preserves band thresholds; underground signals are anecdotal and not stackable into the rubric | Phase 0.7 synthesis carry-forward | R3, R11 |
| 5th post-menu option | Separate "Winning-product dashboard" option — not folded into drill-down | Renders categories ranked by score in a new table view; drill-down (option 1) re-dispatches with `--category=`, which is a different UX shape | Phase 0.7 synthesis carry-forward | R4 |

### Success Criteria

A `/meta-top IN` invocation in v1.3 produces a Section (b) where each category line reads (example):

```
- notion-templates-and-life-os · ₹199–₹1,999 · Score: 11/14 — strong_bet · [longevity 3, variants 2, cross_country 2, engagement 1, marketplace 2, pain_signal 1]
```

And a Section (d) followed by an `Underground signals observed` blockquote with ≥1 cited observation. And the post-menu now offers 5 options including the dashboard.

Same for `/meta-top-digital IN`. The two skills' outputs are visually distinct (the digital version cites Gumroad/Etsy in marketplace signal; the broader meta-top version cites a broader surface) but structurally identical.

### Actors

- **Orchestrator (L1)** — renders Section (b) rubric line, renders underground-signals callout, presents 5-option post-menu.
- **Sub-agent (L2)** — runs WebSearch against the 6+4 canonical queries, classifies each signal per R1, computes `winning_score` per R2, emits underground-signal observations per R3.
- **Region YAML (L3)** — supplies `signal_seeds` for region-specific query phrasing.
- **User** — invokes the skill; reads the rubric; can drill in (option 1) or view the dashboard (option 5).

### Key Flows

```
User: /meta-top IN
  ↓
Orchestrator (SKILL.md)
  ↓ reads region YAML → signal_seeds{}
  ↓ dispatches sub-agent (path only, not content)
Sub-agent (meta-top-researcher.md)
  ↓ reads region YAML → signal_seeds{}
  ↓ runs 6+4 canonical queries
  ↓ classifies 6 signals per category
  ↓ computes winning_score.total + winning_score.band
  ↓ observes underground signals
  ↓ emits JSON digest with new fields
Orchestrator
  ↓ renders Section (b) with per-category rubric line
  ↓ renders underground-signals callout after Section (d)
  ↓ presents 5-option post-menu
User
  ↓ picks option 5 → dashboard renders ranked table
```

### Scope Boundaries

**In scope (R1–R14 above):**

- Per-category 6-signal scoring (R1, R2)
- Underground-signals qualitative callout (R3)
- 5th post-menu option (R4)
- Badge bump v1 → v1.3 (R5)
- Cross-skill parity (R6)
- Sub-agent JSON schema addition (R7)
- 4 new canonical WebSearch queries per sub-agent (R8)
- Region YAML `signal_seeds` field (R9)
- Free-tool-only constraint (R10)
- No historical score tracking (R14)

**Out of scope (deferred to a future plan):**

- Paid-tool integration (Pipiads / MagicBrief / Foreplay / AdSpy / SEMrush / Ahrefs / SparkToro / Tubular Labs / Sensor Tower) — referenced as an "optional upgrade path" in the data-quality footnote, but not queried.
- Historical score tracking across runs (trend lines, week-over-week score changes) — deferred; current snapshot semantics preserved.
- A/B testing framework for ad-creative variants — explicitly out per existing skill contracts.
- Per-creator dashboard (separate from per-category) — explicit user decision to keep at the category level.
- 7th scored underground signal — explicit user decision (qualitative callout instead).
- A separate `meta-top-winning` skill — explicit user decision to fold the framework into the existing two skills rather than spawn a third.

## Planning Contract

### Key Technical Decisions

**KTD1 — Three-layer architecture**. Orchestrator (SKILL.md) → sub-agent (researcher) → region YAML. Mirrors the existing meta-top v1 architecture exactly; no new layer, no new dispatcher.

**KTD2 — Sub-agent is the source of truth for scores**. R12: orchestrator renders, sub-agent computes. Downstream tools can trust `winning_score.total` and `winning_score.band` as deterministic outputs of the digest.

**KTD3 — Region YAML is the source of truth for region-specific query seeds**. R9: `signal_seeds` is additive; existing fields (`top_categories`, `top_brands`, `format_constraints`, etc.) unchanged.

**KTD4 — Per-signal `confidence` is part of the JSON schema, not a derived flag**. Sub-agent emits `confidence: high|medium|low` per signal based on evidence depth (≥2 cited URLs → high; 1 cited URL → medium; 0 cited URLs but signal still inferred from related evidence → low). This makes confidence a first-class signal for downstream consumers.

**KTD5 — No new tools, no new APIs, no new dependencies**. R10: framework uses existing tools only. The `scripts/keyless_search.py` floor and the source ladder (v1.1+) carry the new queries inside the existing 8-source ceiling.

**KTD6 — Badge bumps are intentional, never auto-increment**. R5: v1 → v1.3 is the bump for this change. Future additive changes continue the convention (v1.4, v1.5, etc.).

**KTD7 — Post-menu routing stays inline in SKILL.md**. Per `post-menu-routing-belongs-inline` learning. Option 5 routing (re-render section-(b) categories as a sorted Markdown table, in-chat, no dispatch) lives in Step 4 of SKILL.md.

**KTD8 — `winning_score` is fail-soft under thin data**. R13: missing signals score 0; orchestrator surfaces `confidence: low` inline rather than failing closed. This preserves the existing `partial_research` semantics from the source ladder.

### High-Level Technical Design

Three-layer architecture with additive JSON schema and additive YAML field. No new files, no new modules, no new dependencies.

**JSON schema extension (sub-agent → orchestrator).** Both researcher specs gain `winning_signals` and `winning_score` per `top_categories[]` entry. The shape:

```json
{
  "name": "notion-templates-and-life-os",
  "positioning_note": "...",
  "pricing_examples": [...],
  "evidence_urls": [...],
  "winning_signals": {
    "longevity":    { "sub_score": 3, "evidence_urls": ["url1", "url2"], "confidence": "high" },
    "variants":      { "sub_score": 2, "evidence_urls": ["url1"],         "confidence": "medium" },
    "cross_country": { "sub_score": 2, "evidence_urls": ["url1", "url2"], "confidence": "high" },
    "engagement":    { "sub_score": 1, "evidence_urls": ["url1"],         "confidence": "medium" },
    "marketplace":   { "sub_score": 2, "evidence_urls": ["url1"],         "confidence": "medium" },
    "pain_signal":   { "sub_score": 1, "evidence_urls": ["url1"],         "confidence": "low" }
  },
  "winning_score": {
    "total": 11,
    "band": "strong_bet",
    "computed_at": "2026-09-27"
  },
  "underground_signals": [
    { "kind": "scarcity_working", "observation": "Ad copy flips 'sold out' -> 'back again' every 3-4 days", "evidence_url": "url1" },
    { "kind": "creator_collab_to_paid", "observation": "Reel reshared as ad after 240K organic views", "evidence_url": "url2" }
  ]
}
```

`underground_signals[]` is parallel to `winning_signals`; it carries the R3 callout observations. Empty array is valid (orchestrator omits the callout blockquote in that case).

**YAML schema extension (region YAML → sub-agent).** Each region YAML gains a `signal_seeds` block:

```yaml
signal_seeds:
  longevity:    "<query template>"
  variants:     "<query template>"
  cross_country:"<query template>"
  engagement:   "<query template>"
  marketplace:  "<query template>"
  pain_signal:  "<query template>"
```

Six string templates per region; `{category}` is the runtime substitution token. The 12 region YAMLs (6 per skill) each get their own set — region-specific search phrasing is the whole point of moving seeds into YAML rather than hard-coding in the researcher spec.

**Orchestrator rendering (SKILL.md).** Section (b) gains a per-line rubric:

```
- {category-name} · {currency}{price-range} · Score: {X}/14 — {band} · [{signal breakdown}]
```

Underground-signals callout after Section (d):

```
> **Underground signals observed**
> - {kind}: {observation} ([source]({url}))
> - {kind}: {observation} ([source]({url}))
```

Post-menu Step 4 grows to 5 options:

```
1. Drill into a category — ...
2. Save HTML brief — ...
3. Export creative pack — ...
4. Winning-product dashboard — render section-(b) categories sorted by score
5. Done for now — ...
```

### Assumptions

- **A1.** Sub-agent already caps sources at 8 per invocation; the 4 new queries fit within that ceiling alongside the existing 6 (no source-cap regression).
- **A2.** Both skills' current JSON schemas are tolerant of additive fields — verified by reading both researcher specs (they emit a single JSON object to stdout, and the orchestrator renders named fields, not positionally indexed arrays).
- **A3.** Meta Ad Library, Gumroad, Etsy, Reddit, Google Trends remain accessible without auth in 2026 (no rate-limit ceiling that breaks the source ladder).
- **A4.** The 30-minute weekly refresh workflow (per the user's ARGUMENTS) is the user's target cadence — informs confidence thresholds but does not gate the plan.
- **A5.** The 14-max ceiling and band thresholds (9+ / 6–8 / <6) are user-specified and not subject to user review during this plan.

## Implementation Units

> **U-ID stability.** `U1–U17` are stable across re-renders. New units get `U18+`. Do not renumber existing units.

### U1. Update `meta-top` orchestrator SKILL.md — badge, Section (b) rubric, underground callout, post-menu option 5

**Goal:** Apply R5 (badge v1 → v1.3), R1 (per-category rubric rendering in Section (b)), R3 (underground-signals callout after Section (d)), R4 (5th post-menu option).

**Files:**

- `C:\Users\HP\projects\meta-top\skills\meta-top\SKILL.md`

**Approach:**

1. SKILL Contract item 1 — change `v1` to `v1.3`.
2. SKILL Contract item 8 — change `four options` to `five options`; reference new option 5 inline.
3. Step 2 item 2 — append per-line rubric template: `Score: {X}/14 — {band} · [longevity {a}, variants {b}, cross_country {c}, engagement {d}, marketplace {e}, pain_signal {f}]`.
4. Step 2 item 4 (Specific product examples) — add a new sub-item 4a: "Underground signals observed. If `underground_signals[]` is non-empty in the digest, render a `> **Underground signals observed**` blockquote listing each observation with its source. Empty array → omit the blockquote."
5. Step 4 (Post-Menu Routing) — add option 5 inline: "Winning-product dashboard — re-render section-(b) categories as a Markdown table sorted by `winning_score.total` descending: `| Score | Band | Category | Top signal | Sources |`. Read each category's `winning_signals`, find the sub-signal with the highest sub_score, label it as `Top signal`. Read `evidence_urls` count for the `Sources` column. Inline render in chat, no dispatch."
6. Hard-Block section — no change.
7. Reliability / source ladder — no change (sub-agent absorbs the new queries; the 8-source ceiling applies).

**Test Scenarios:**

- T-U1.1 — Section (b) line format matches: `- {category} · {price} · Score: {X}/14 — {band} · [{breakdown}]`.
- T-U1.2 — Section (d) followed by an `Underground signals observed` blockquote when the digest's `underground_signals[]` is non-empty; omitted when empty.
- T-U1.3 — Post-menu presents 5 options; option 5 description includes "Winning-product dashboard".
- T-U1.4 — Badge line 1 reads `v1.3`.

**Verification:**

- `grep -n "v1.3" skills/meta-top/SKILL.md` returns the badge line.
- `grep -n "Score: {X}/14" skills/meta-top/SKILL.md` returns Section (b) template.
- `grep -n "Winning-product dashboard" skills/meta-top/SKILL.md` returns Step 4 routing.
- `grep -n "Underground signals observed" skills/meta-top/SKILL.md` returns new sub-item 4a.

### U2. Update `meta-top-researcher.md` sub-agent spec — Step 3c Signal Extraction, 4 new queries, JSON schema

**Goal:** Apply R7 (JSON schema addition), R8 (4 new canonical queries).

**Files:**

- `C:\Users\HP\projects\meta-top\skills\meta-top\references\agents\meta-top-researcher.md`

**Approach:**

1. Step 3 — extend the seed query list from 6 to 10 by appending 4 new queries (longevity-specific, variants-specific, cross-country-specific, pain-signal-specific). The existing 6 stay in their declaration order.
2. Add Step 3c — Signal Extraction. For each `top_categories[]` entry, run the region-YAML `signal_seeds` queries (or fall back to the canonical queries from Step 3) and classify each of the 6 signals. Emit `winning_signals`, `winning_score`, and `underground_signals` per the JSON schema below.
3. Step 4 (Classify and structure JSON) — extend the `top_categories[]` item schema with three new keys: `winning_signals`, `winning_score`, `underground_signals`.
4. Step 5 (Transparency) — extend the data-quality-note example to mention `winning_score` confidence distribution when thin data is involved.
5. Output Size — keep the digest at 5–15 KB; the new fields add ~500 bytes per category.

**Test Scenarios:**

- T-U2.1 — Step 3 lists 10 seed queries.
- T-U2.2 — Step 3c exists and references `signal_seeds` from the region YAML.
- T-U2.3 — JSON schema for `top_categories[]` item includes `winning_signals`, `winning_score`, `underground_signals`.
- T-U2.4 — Sub-score maxes per signal match R1 (longevity max 3, variants max 3, cross_country max 2, engagement max 2, marketplace max 2, pain_signal max 2; total max 14).

**Verification:**

- `grep -n "winning_signals" skills/meta-top/references/agents/meta-top-researcher.md` returns the JSON schema.
- `grep -n "Step 3c" skills/meta-top/references/agents/meta-top-researcher.md` returns the new step.

### U3–U8. Add `signal_seeds` to 6 meta-top region YAMLs

**Goal:** Apply R9 (region YAML additive field). Six YAMLs: `in`, `us`, `ca`, `uk`, `au`, `ae`.

**Files (one per unit, separate U-IDs for stable addressing):**

- `C:\Users\HP\projects\meta-top\skills\meta-top\references\regions\in.yaml` (U3)
- `C:\Users\HP\projects\meta-top\skills\meta-top\references\regions\us.yaml` (U4)
- `C:\Users\HP\projects\meta-top\skills\meta-top\references\regions\ca.yaml` (U5)
- `C:\Users\HP\projects\meta-top\skills\meta-top\references\regions\uk.yaml` (U6)
- `C:\Users\HP\projects\meta-top\skills\meta-top\references\regions\au.yaml` (U7)
- `C:\Users\HP\projects\meta-top\skills\meta-top\references\regions\ae.yaml` (U8)

**Approach:** Insert a `signal_seeds` block (6 keys) at the bottom of each YAML, above `last_reviewed`. The seeds use region-specific search phrasing — Indian YAML uses Hindi/Hinglish site filters and Topmate; US/UK/CA/AU use English phrasing and G2/Product Hunt; AE uses bilingual phrasing where relevant.

Example for `in.yaml` (U3):

```yaml
signal_seeds:
  longevity: "site:facebook.com/ads/library India {category} active 90 days"
  variants: "{category} India Meta ads variants scaling"
  cross_country: "{category} Meta ads US UK CA AU running"
  engagement: "{category} India Meta ad comments link please"
  marketplace: "{category} India Gumroad Instamojo Topmate trending 2026"
  pain_signal: "{category} India reddit r/IndianInvestments r/developersIndia"
```

**Test Scenarios:**

- T-U{3-8}.1 — YAML parses cleanly (no syntax errors).
- T-U{3-8}.2 — All 6 signal keys present: `longevity`, `variants`, `cross_country`, `engagement`, `marketplace`, `pain_signal`.
- T-U{3-8}.3 — Each value contains `{category}` substitution token.

**Verification:**

- `python -c "import yaml; yaml.safe_load(open('skills/meta-top/references/regions/{region}.yaml'))"` exits 0.
- `grep -n "signal_seeds" skills/meta-top/references/regions/{region}.yaml` returns the block.

### U9. Update `meta-top-digital` orchestrator SKILL.md — mirror U1 with digital-only phrasing

**Goal:** Apply R6 (cross-skill parity). Mirror U1 for the digital sibling.

**Files:**

- `C:\Users\HP\.claude\skills\meta-top-digital\SKILL.md`

**Approach:** Same as U1, but the underground-signals callout uses digital-context phrasing (template scarcity, Notion-template churn, prompt-pack velocity) instead of broader D2C. The post-menu option 5 dashboard renders the same shape (categories ranked by score).

**Test Scenarios:** Same as U1, applied to `meta-top-digital/SKILL.md`.

**Verification:** Same as U1.

### U10. Update `meta-top-digital-researcher.md` sub-agent spec — mirror U2 with digital-only seed queries

**Goal:** Apply R6, R7, R8 for the digital sibling.

**Files:**

- `C:\Users\HP\.claude\skills\meta-top-digital\references\agents\meta-top-digital-researcher.md`

**Approach:** Same as U2. The 4 new digital-only queries (per R8) replace the meta-top broader-D2C queries.

**Test Scenarios:** Same as U2, applied to `meta-top-digital-researcher.md`.

**Verification:** Same as U2.

### U11–U16. Add `signal_seeds` to `meta-top-digital` region YAMLs

**Goal:** Apply R9 for the digital sibling. Only `in.yaml` is currently shipped (U11); `us`, `ca`, `uk`, `au`, `ae` arrive via separate units (U12–U16) — one per region, mirroring the U3–U8 structure.

**Files (one per unit):**

- `C:\Users\HP\.claude\skills\meta-top-digital\references\regions\in.yaml` (U11)
- `C:\Users\HP\.claude\skills\meta-top-digital\references\regions\us.yaml` (U12)
- `C:\Users\HP\.claude\skills\meta-top-digital\references\regions\ca.yaml` (U13)
- `C:\Users\HP\.claude\skills\meta-top-digital\references\regions\uk.yaml` (U14)
- `C:\Users\HP\.claude\skills\meta-top-digital\references\regions\au.yaml` (U15)
- `C:\Users\HP\.claude\skills\meta-top-digital\references\regions\ae.yaml` (U16)

> **NOTE:** The mirror YAMLs for `us/ca/uk/au/ae` are scheduled to ship via a separate U5 mirror unit in the meta-top-digital plan. They are not yet on disk. This plan creates the `signal_seeds` block within the existing `in.yaml` (U11). If U12–U16 are not yet on disk at execution time, those units are deferred — they become trivial (just append `signal_seeds` to a stub YAML) when the mirror ships. Mark them as "blocked on parent mirror unit" in the handoff if needed.

**Approach:** Same as U3, but with digital-marketplace phrasing (Gumroad, Etsy, Notion Marketplace, Canva Creators, Instamojo, Topmate for IN; Creative Market for US/EU).

**Test Scenarios:** Same as U3–U8.

**Verification:** Same as U3–U8.

### U17. Integration smoke test — both skills, both regions (IN + US), all 5 post-menu options

**Goal:** Confirm the v1.3 framework ships end-to-end in both skills.

**Files:** (no file changes; this unit verifies U1–U16)

**Approach:**

1. Invoke `/meta-top IN` via the Skill tool. Verify:
   - Badge line 1 reads `📊 meta-top v1.3 · region: in · 2026-09-27`.
   - Section (b) carries per-category `Score: X/14 — band` rubric lines.
   - Section (d) is followed by an `Underground signals observed` blockquote (when the live research surfaces underground signals; otherwise omitted).
   - Post-menu presents 5 options including "Winning-product dashboard".
2. Pick option 5 from the post-menu. Verify the dashboard renders a Markdown table sorted by score descending.
3. Repeat for `/meta-top US`.
4. Invoke `/meta-top-digital IN`. Verify the same four checks.
5. (Optional) `/meta-top-digital US` — only runs if `us.yaml` exists in the digital sibling (likely blocked on the parent mirror unit; skip with a `data_quality_note: digital-mirror-not-shipped` if missing).

**Test Scenarios:**

- T-U17.1 — Badge reads `v1.3`.
- T-U17.2 — Section (b) rubric line format matches the template.
- T-U17.3 — Post-menu option count = 5.
- T-U17.4 — Dashboard renders ranked table with at least one category.
- T-U17.5 — Both skills' invocations succeed without crashing.

**Verification:**

- Manual invocation; no automated test infrastructure exists for skill prose behavior (per the `skill-eval` family — fresh-agent eval is the portable path; not in scope for this plan).

## Verification Contract

**VC1 — File-existence and parse-time checks** (mechanical, runnable in this session):

```bash
# Both skills' SKILL.md carry the new badge
grep -n "v1.3" "C:/Users/HP/projects/meta-top/skills/meta-top/SKILL.md"
grep -n "v1.3" "C:/Users/HP/.claude/skills/meta-top-digital/SKILL.md"

# Both skills' SKILL.md carry the new Section (b) rubric template
grep -n "Score: {X}/14" "C:/Users/HP/projects/meta-top/skills/meta-top/SKILL.md"
grep -n "Score: {X}/14" "C:/Users/HP/.claude/skills/meta-top-digital/SKILL.md"

# Both skills' SKILL.md carry the new post-menu option 5
grep -n "Winning-product dashboard" "C:/Users/HP/projects/meta-top/skills/meta-top/SKILL.md"
grep -n "Winning-product dashboard" "C:/Users/HP/.claude/skills/meta-top-digital/SKILL.md"

# Both researcher specs carry the new JSON schema
grep -n "winning_signals" "C:/Users/HP/projects/meta-top/skills/meta-top/references/agents/meta-top-researcher.md"
grep -n "winning_signals" "C:/Users/HP/.claude/skills/meta-top-digital/references/agents/meta-top-digital-researcher.md"

# All 6 meta-top region YAMLs carry signal_seeds
for region in in us ca uk au ae; do
  grep -n "signal_seeds" "C:/Users/HP/projects/meta-top/skills/meta-top/references/regions/${region}.yaml"
done

# The shipped digital region YAML carries signal_seeds
grep -n "signal_seeds" "C:/Users/HP/.claude/skills/meta-top-digital/references/regions/in.yaml"

# YAML parses cleanly (Python yaml.safe_load)
python -c "import yaml; yaml.safe_load(open('C:/Users/HP/projects/meta-top/skills/meta-top/references/regions/in.yaml'))"
python -c "import yaml; yaml.safe_load(open('C:/Users/HP/.claude/skills/meta-top-digital/references/regions/in.yaml'))"
```

**VC2 — End-to-end smoke (U17 invocation).** Run `/meta-top IN` and `/meta-top-digital IN` via Skill tool. Confirm the badge, Section (b) rubric, underground callout (when present), and 5-option post-menu. This is manual in this session; future `ce-work` runs of this plan can also re-execute.

**VC3 — Skill prose behavior** (out of scope for automated verification, per `bun run test` does not exercise skill prose). Fresh-agent eval (`bun run test:skill-eval-cell` or `bun run test:skill-eval-pack -- --skill meta-top --arm ab`) is the portable path for cross-model behavioral validation. Not gated by this plan.

## Definition of Done

A run is complete when:

1. **Files modified.** All 14 files in U1–U16 carry their intended changes:
   - `skills/meta-top/SKILL.md` (U1)
   - `skills/meta-top/references/agents/meta-top-researcher.md` (U2)
   - `skills/meta-top/references/regions/{in,us,ca,uk,au,ae}.yaml` (U3–U8)
   - `~/.claude/skills/meta-top-digital/SKILL.md` (U9)
   - `~/.claude/skills/meta-top-digital/references/agents/meta-top-digital-researcher.md` (U10)
   - `~/.claude/skills/meta-top-digital/references/regions/in.yaml` (U11)
   - `~/.claude/skills/meta-top-digital/references/regions/{us,ca,uk,au,ae}.yaml` (U12–U16, blocked on parent mirror unit; if mirror not shipped, these units are deferred)
2. **Badge updated.** Both skills' line 1 reads `v1.3`.
3. **Schema extension.** Both researcher specs emit `winning_signals`, `winning_score`, `underground_signals` per `top_categories[]` entry.
4. **Region YAMLs extended.** All 6 meta-top region YAMLs carry `signal_seeds{}` with 6 keys. The shipped meta-top-digital region YAML (`in.yaml`) carries `signal_seeds{}`.
5. **Render verification.** VC1 grep checks return matches for both skills. VC1 YAML parses exit 0.
6. **Smoke verification (U17).** `/meta-top IN` and `/meta-top-digital IN` invocations render the v1.3 shape end-to-end. Manual verification; no automated gate.
7. **No regressions.** Existing hard-blocks still fire (e.g., `category-pricing-research-required` for the digital sibling); existing SKILL contract items 1–7 (other than item 1's badge and item 8's menu count) are unchanged.

## Cross-References

- Source framework provided in the user's ARGUMENTS — see Phase 0.7 synthesis carry-forward and Key Decisions table.
- Existing skill contracts: `skills/meta-top/SKILL.md` (v1) and `~/.claude/skills/meta-top-digital/SKILL.md` (v1).
- Source ladder (existing v1.1+ mechanics): `scripts/keyless_search.py` and the 4-tier (5-tier for digital) ladder in each SKILL.md.
- Existing hard-block: `category-pricing-research-required` in `meta-top-digital-researcher.md` line ~207 — preserved.
- `post-menu-routing-belongs-inline` learning: Step 4 routing stays in SKILL.md, never in `references/`.
- `pass-paths-not-content-to-subagents` learning: orchestrator hands sub-agent the absolute YAML path; sub-agent reads it.
