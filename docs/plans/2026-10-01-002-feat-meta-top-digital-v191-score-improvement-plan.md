---
title: "meta-top-digital v1.9.1 — Sharpen winning-product signals for thin-data regions - Plan"
type: feat
date: 2026-10-01
artifact_contract: ce-unified-plan/v1
product_contract_source: ce-plan-bootstrap
execution: code
---

> **Path convention.** All paths are relative to the live skills root `C:\Users\HP\.claude\skills\` (what `/meta-top-digital` actually loads). The working-copy mirror at `C:\Users\HP\projects\meta-top\skills\` is the version-controlled draft. **Every unit's verification ends with a live-path grep AND a `cp -f` mirror sync** per the `meta-top-skill-file-paths` memory rule.

## Goal Capsule

**Objective.** Lift the three weakest winning-product signals — `cross_country`, `engagement`, `pain_signal` — from their current 0–1 sub-scores to 1–2 each, so the winning-product verdict callout reflects a meaningful confidence/band picture for thin-data regions like India. Today the top-3 categories sit at 4–5/14 ("skip" band) because cross_country and pain_signal are uniformly 0 across the board.

**Means.** Make the cross-region sweep (IN+US+UK per top-3 category) MANDATORY rather than OPTIONAL, lifting the `cross_country` signal from 0 to 1–2 per top-3 category. Tier-0 sub-budget rebalances to: category-level ≤3 (top-3 only), cross-region ≤9 (3 regions × top-3), retry ≤1, total ≤13. Add a one-line gloss to the brief's per-category rubric line + a conditional gloss to the verdict callout so the score/band/confidence contradiction is no longer read as confusing. The v1.9.1 scope is narrower than originally drafted: Playwright probes confirmed U2 (FB Group engagement) and U3 (Reddit/Quora pain scraping) cannot reach their target data via Playwright in IN (reCAPTCHA wall on Reddit; private/login-walled on FB Groups; 404 on Quora topic URLs). Those sub-routes defer to v1.9.2 with a redesigned surface approach. (U1, U2, U3)

**Authority hierarchy.** This plan inherits v1.9's ladder design, hard-block semantics, F16 baseline logging, and confidence formula. It does NOT supersede v1.5's `pricing_tier_source` enum or v1.6's verdict callout. v1.9.1 is additive on the scoring side, not the pricing or verdict side.

**Stop conditions.** Hard-block gate (0 of 3 observed_live → `category-pricing-research-required`) is unchanged. Latency budget ≤120s is unchanged (per the v1.9 KTD3 settled decision). Tier-0 cap ≤13 is unchanged. F16 baseline log continues unchanged; v1.9.1's contribution is observable as additional sub-route outcomes recorded under `data_quality_note`.

**Execution profile.** code, ~5 implementation units, ships in one focused work session.

**Who finishes and ships.** The next `/ce-work` invocation against this plan.

## Product Contract

### Summary

Lift the `cross_country` winning-product signal from 0 to 1–2 per top-3 category by making the cross-region sweep (IN+US+UK per top-3) MANDATORY rather than OPTIONAL. The other two originally-targeted signals (`engagement`, `pain_signal`) defer to v1.9.2 because Playwright probes confirmed their target surfaces (FB Groups, Reddit, Quora) are not reachable for IN. Also tighten the brief's explanation of the score/band/confidence relationship so the "Score 5/14 — skip" + "Confidence 90% — winning-grade" surface is no longer read as confusing. Tier-0 sub-budget rebalances to category-level ≤3 + cross-region ≤9 + retry ≤1 = ≤13, honoring v1.9 KTD2's unconditional ≤13 invariant.

### Problem Frame (revised)

The v1.9 India run produced winning_scores of 4 (notion-templates), 5 (prompt-packs), 5 (spreadsheet), 6 (canva-templates), and 7 (ebook-bundles). The verdict callout named spreadsheet as the winner with 90% confidence ("winning-grade"), yet the score band reads "skip" (<6). The mismatch reads as contradictory even though it isn't — the rubric bands measure ad-inventory strength, while the confidence formula measures defensibility of the choice. The user encountered this in the post-brief clarification and asked how to improve the score.

Initial analysis identified three weak signals (cross_country=0, engagement=0–1, pain_signal=0). Plan v1.9.1 first draft targeted all three with new tier-0 sub-routes. Playwright probe results (2026-10-01) invalidated two of those sub-routes for IN:

- Reddit `/r/Notion` serves a reCAPTCHA wall; no post/comment data exposed.
- Quora `/Notion-templates` returns HTTP 404.
- Facebook `/groups/notiontemplates/` returns "content not available right now" — private/login-walled.

Empirically, only `cross_country` (the cross-region sweep via Meta Ad Library) has a viable Playwright surface for IN. The original three-signal scope narrows to one-signal scope for v1.9.1.

### Problem Frame

The v1.9 India run produced winning_scores of 4 (notion-templates), 5 (prompt-packs), 5 (spreadsheet), 6 (canva-templates), and 7 (ebook-bundles). The verdict callout named spreadsheet as the winner with 90% confidence ("winning-grade"), yet the score band reads "skip" (<6). The mismatch reads as contradictory even though it isn't — the rubric bands measure ad-inventory strength, while the confidence formula measures defensibility of the choice. The user encountered this in the post-brief clarification and asked how to improve the score.

Original three root causes:

1. **cross_country = 0 universally.** The v1.5 cross-region sweep was made OPTIONAL in v1.8 ("when time budget is tight, the researcher skips the cross-region sweep"). For IN the time-budget is always tight, so the sweep is always skipped. Without it, no top-3 category can score above 0 on cross_country. **v1.9.1 addressable — Meta Ad Library is publicly accessible via Playwright.**

2. **engagement = 0–1 universally.** Tier-0 (Meta Ad Library via Playwright) renders ad cards but does not surface comment threads. WebSearch rate-limited in the v1.9 IN run. The probe alternative (FB Group scraping) is private/login-walled; cannot reach comment data. **v1.9.1 deferred to v1.9.2 — needs redesigned surface.**

3. **pain_signal = 0 universally.** Playwright probe (2026-10-01) confirms Reddit reCAPTCHA walls, Quora topic URLs return 404, no public path to discussion signal. Tier-1 WebSearch returned 0 results across 4 queries in v1.9 IN run. **v1.9.1 deferred to v1.9.2 — needs redesigned surface.**

The cap (≤13 navs, ≤120s) is not the bottleneck — v1.9 IN used ~115s for tier-0 per F16 baseline. The cross-region MANDATORY change reallocates the existing nav budget, no cap raise needed.

### Requirements

**Signal extraction (R1).**

- R1. The cross-region sweep (IN + US + UK per top-3 category) MUST be MANDATORY rather than OPTIONAL. ≤9 tier-0 navs allocated (3 regions × top-3 categories), folded into the same ≤13 sub-budget. The `cross_country` sub-score MUST use observed-advertiser-overlap data from the sweep, not the proxy heuristics used in v1.5.

**Tier-0 sub-budget rebalance (R2).**

- R2. The tier-0 sub-budget allocation MUST change to absorb R1 within the ≤13 cap:
  - Category-level: ≤5 → ≤3 (top-3 only, was top-5)
  - Marketplace-level: ≤4 → 0 (dropped — v1.9 IN run surfaced Instamojo D2C pivot, Notion login wall, Canva Creators no INR prices; marketplace navs had thin yield)
  - Open-ended: ≤2 → 0 (dropped — search engines block Playwright aggressively; tier-1 WebSearch remains as confirmation)
  - Cross-region: 0 → ≤9 (mandatory, R1)
  - Retry: ≤2 → ≤1 (reduced to fit ≤13)
  - Total ≤13 (unchanged)

**Brief surface (R3).**

- R3. The brief's per-category rubric line MUST include a one-line gloss explaining the score/band/confidence relationship, so the user no longer encounters the "skip" + "winning-grade" contradiction as confusing. The gloss MUST be present in every v1.9.1+ brief.

**Mirror parity (R4).**

- R4. The working-copy mirror at `C:\Users\HP\projects\meta-top\skills\meta-top-digital\` MUST match live `C:\Users\HP\.claude\skills\meta-top-digital\` byte-for-byte after each unit lands, per the `meta-top-skill-file-paths` memory rule.

### Scope Boundaries

#### In scope

- Cross-region sweep made MANDATORY for top-3 (R1).
- Tier-0 sub-budget rebalance to absorb R1 within ≤13 cap (R2).
- Brief surface gloss for score/band/confidence relationship (R3).
- Mirror parity discipline (R4).

#### Explicitly deferred from v1.9.1 (per Playwright probe 2026-10-01)

- **Engagement sub-route (FB Group scraping).** Probe confirms FB Groups are private/login-walled; cannot reach comment data via Playwright. Redesign in v1.9.2 — candidate surfaces: public FB Pages (vs Groups), Slack/Discord public communities, X/Twitter public timelines, region-specific forums.
- **Pain-signal sub-route (Reddit/Quora scraping).** Probe confirms Reddit reCAPTCHA walls, Quora topic URLs return 404. Redesign in v1.9.2 — candidate surfaces: Lemmy/Kbin (Reddit alternatives), open Reddit mirrors, public subreddits that bypass verification, region-specific Quora topics.

#### Deferred to Follow-Up Work

- **Confidence-formula recalibration.** Per the v1.6 plan Q1 / v1.9 deferred — gated on ≥30 invocations of F16 baseline data showing formula compression. Not enough data yet (3 IN invocations logged). Hold for v1.9.2.
- **Hard-block threshold relaxation** (0/3 → 1/3 → brief ships). Per the v1.8 plan Q3 / v1.9 deferred — same gate. Hold for v1.9.2.
- **Marketplace list refresh.** The v1.9 IN run surfaced Instamojo pivot, Notion login wall, Canva Creators no-INR-prices. A fresh regional marketplace audit (Topmate, IndiaMART digital, FreePixel, regional Gumroad subdomains) is its own planning effort. Out of scope for v1.9.1; explicitly deferred.
- **Rubric band threshold changes** ("skip" / "promising" / "strong_bet" cutoffs). The current bands are calibrated to data-rich regions (US/UK). Adjusting them for thin-data regions is a calibration question, not a v1.9.1 question. Hold for v1.9.2 once F16 data validates.
- **meta-top (parent skill) parity.** meta-top has a different category shape (physical D2C) and a different cross-region opportunity. The cross-region sweep's relevance to meta-top is a separate decision. Out of scope for v1.9.1.

#### Outside this product's identity

- Removing the trust + ethics frame.
- Removing the per-category observed-live hard-block (relaxing the threshold is in-scope as future work; removing the block is not).
- Removing the prohibition on cloning specific creator content from the Option B brief.
- Changing the six-section output structure (a–f).
- Changing the badge format.
- Changing the v1 region list.
- Multi-language output.
- Meta Business Manager API integration.

### Acceptance Examples

- AE1. The cross-region sweep runs on all top-3 categories for IN, producing ≥1 advertiser overlap observation per category AND ≥1 same-niche category-keyword match in the overlap (not just any same-platform ad). The `cross_country` sub-score reaches ≥1 on at least one top-3 category.
- AE4. After R1 fires on a simulated IN run, the spreadsheet top-3 winning_score reaches ≥7/14 ("promising" band), up from 5/14 ("skip" band) in v1.9. (5 baseline + crosscountry 0→2 = 7.) Engagement and pain_signal lifts deferred to v1.9.2.
- AE5. The brief's verdict callout renders the conditional gloss (per U3) when the named winner has 'skip' band + 'winning-grade' confidence. The per-category rubric-line gloss (per R3) is always-on and renders on every category regardless of discrepancy.
- AE6. Tier-0 total nav count stays ≤13 with R1 active. Sub-cap allocation matches R2.
- AE7. A simulated IN run completes tier-0 within ≤120s wall-clock time, with F16 baseline recording actual latency per sub-route. Latency overruns block Definition of Done item 4 (not just nav count).

## Planning Contract

### Key Technical Decisions

- KTD1. Cross-region sweep made MANDATORY rather than OPTIONAL (R1). Rationale: the v1.8 OPTIONAL gate was authored under the assumption that "when time budget is tight, the researcher skips the cross-region sweep." With v1.9's ≤120s latency budget and tier-0 measured at ~115s for IN, time budget is always tight for thin-data regions, so OPTIONAL means "always skipped for IN." Making it MANDATORY recovers the cross_country signal deterministically. Cost: 9 of 13 tier-0 navs spent on cross-region (3 regions × top-3); the remaining 4 navs cover category-level (≤3) + retry (≤1). (session-settled: user-directed — "do what is needed to make the slash command better in research, finding pain points and finding a winning product".)

- KTD2. Marketplace-level tier-0 dropped (R2). Rationale: the v1.9 IN run surfaced 1 successful marketplace nav out of 4 (Gumroad, but priced in CAD not INR). Instamojo pivoted to D2C site builder. Notion Marketplace requires login (verification wall). Canva Creators has no public INR prices. Marketplace navs have thin yield for IN; the budget reallocates to cross-region (the only viable v1.9.1 sub-route). Trade-off: lose marketplace-side signals (creator velocity, royalty model, regional curation). Recoverable in v1.9.2 via the deferred marketplace-list-refresh work.

- KTD3. Open-ended tier-0 dropped (R2). Rationale: search engines (Google, Bing, DuckDuckGo) block Playwright aggressively; the v1.8 KD3 anticipated tier-1 (WebSearch) fallback when blocked. With tier-1 WebSearch already failing for IN (0 results across 4 queries in v1.9 IN run per F16 baseline), the open-ended tier-0 sub-route has no fallback path that produces signal. (session-settled: design synthesis — derived from v1.9 IN run observed failure mode.)

- KTD4. Category-level reduced from top-5 to top-3 (R2). Rationale: the rubric band (skip / promising / strong_bet) is computed on top-3, so top-5 navs beyond top-3 produce data that doesn't drive scoring. With 9 navs going to cross-region (which covers top-3 explicitly), the top-5 category navs become redundant — top-3's cross-region coverage is denser than top-5's flat coverage. Trade-off: lose ad-inventory breadth on 4th and 5th categories; gain depth on top-3.

- KTD5. Retry reduced from ≤2 to ≤1 (R2). Rationale: with cross-region consuming 9 navs and category-level 3, only 1 nav remains for retry. Trade-off: a single Playwright failure on either sub-route cascades (no recovery nav). Acceptable given v1.9.1's narrowed scope (only cross-region is critical; category-level failure is non-fatal).

- KTD6. U2 (FB Group engagement) and U3 (Reddit/Quora pain) deferred to v1.9.2 — empirically invalidated by Playwright probe 2026-10-01. Reddit reCAPTCHA walls, FB Groups private/login-walled, Quora topic URLs return 404. v1.9.2 must redesign surfaces (public FB Pages, Slack/Discord, X/Twitter, Lemmy/Kbin, open Reddit mirrors, region-specific forums). v1.9.1 scope: cross-region sweep only.

- KTD7. Brief surface gloss (R3) is one line, not a paragraph. Rationale: prose-economy discipline (no per-KTD precedent in v1.9 — neither the live SKILL.md nor any prior plan enshrines a one-line-gloss rule; this KTD introduces the convention). The gloss explains: "score = ad-inventory strength; confidence = defensibility-of-winner-choice." Trade-off: a one-liner gloss can't fully resolve all band/confidence edge cases; the user is expected to read Section (b) for the full rubric.

- KTD8. v1.9.1 ships as `v1.9 → v1.9.1`. Rationale: v1.9.1 is a signal-extraction sharpening (one signal: cross_country), not a ladder redesign or scoring-rubric change. Minor version bump aligns with the user's mental model (v1.9 was the trigger widening + cap raise; v1.9.1 is the scoring sharpening). Both paths bump (live `C:\Users\HP\.claude\skills\` + working-copy `C:\Users\HP\projects\meta-top\skills\` mirror per the `meta-top-skill-file-paths` memory rule) — NOT both skills (meta-top is explicitly out-of-scope per Scope Boundaries).

### High-Level Technical Design

A swim-lane sequence of v1.9.1's tier-0 flow (≤13 navs total):

```
+-----------------------+-----+-----+-----+-----+
| Sub-route             | cat 1 | cat 2 | cat 3 | retry |
+-----------------------+-----+-----+-----+-----+
| Meta Ad Library       | 1   | 1   | 1   | -     |  <=3 navs
| Cross-region sweep    | 1+1+1|1+1+1|1+1+1| -     |  <=9 navs (3 regions)
| Retry reserve         | -   | -   | -   | 1     |  <=1 nav
+-----------------------+-----+-----+-----+-----+
| Total                 |     |     |     |       |  <=13 navs
```

Top-3 category always gets the full sweep (Meta Ad Library + 3-region cross-region). The retry reserve covers a single Playwright failure. Sub-cap priority rule: cross-region sweep MUST fire on top-3 before retry can claim any nav.

The cross-region sweep follows the existing round-robin marketplace rotation logic (F11) extended to regions: IN → US → UK per category in deterministic order, deduped against any URL previously tier-0 visited this invocation.

### Assumptions

- The Playwright MCP server (`mcp__plugin_playwright_playwright__browser_*`) remains available in the host environment. If unavailable, R1 falls through to tier-1 (WebSearch) per the existing v1.9 fail-soft behavior. The `data_quality_note` records which sub-routes fell through.
- FB Group / Page threads render buyer-intent comments in the a11y tree under the standard Facebook commenting widget. If Facebook changes the widget structure between snapshots, R2's parsing logic may break; the implementer should snapshot one IN FB Group before authoring and confirm the comment-card structure.
- Reddit's a11y tree exposes subreddit post titles + comment counts + comment text in the standard `/r/<subreddit>` listing page. If Reddit adds a JS-rendered wall (verified wall, captcha), R3 falls through to tier-1 WebSearch.
- 3 category-level navs × ~7-9s/nav + 9 cross-region navs × ~7-9s/nav + 1 retry nav × ~7-9s/nav = ~91-117s worst case (depending on per-nav variance). F16 baseline shows v1.9 IN tier-0 used ~115s for ≤13 navs (~8.8s/nav actual). v1.9.1 uses 13 navs at ~8.8s/nav = ~114s, within the ≤120s budget with ~6s margin. If the actual per-nav latency exceeds ~9.2s on average, the budget overruns and F16 baseline records the overrun.
- The per-region `signal_seeds` block in the region YAML lists the appropriate subreddit defaults. v1.9.1 uses the `in.yaml` defaults for IN; future regions author their own `signal_seeds.pain_signal` lists.

## Implementation Units

### U1. Make cross-region sweep MANDATORY for top-3 categories (cross_country)

**Goal.** Lift `cross_country` from 0 to 1-2 per top-3 category by running the IN+US+UK sweep on every invocation.

**Requirements.** R1.

**Files.**
- `meta-top-digital/references/agents/meta-top-digital-researcher.md` - Step 3.0a dispatch policy
- `meta-top-digital/SKILL.md` - Reliability: source ladder section

**Approach.**
- Edit `meta-top-digital-researcher.md` Step 3.0a: change "Cross-region sweep is OPTIONAL in v1.8" to "Cross-region sweep is MANDATORY for top-3 categories in v1.9.1." The implementer also adds explicit sub-cap allocation: <=6 navs (3 regions x top-3).
- Edit `meta-top-digital/SKILL.md` Reliability: source ladder section to mirror the MANDATORY status. The v1.9 OPTIONAL-due-to-time-budget wording is replaced with MANDATORY with budget rationale (KTD1).
- The cross-region sweep uses the existing F11 round-robin logic extended to regions. No new extraction logic - the v1.5 observed-advertiser-overlap scoring carries forward verbatim.

**Patterns to follow.** v1.5 plan R-section on cross-region sweep; v1.9.1 KTD1; existing Step 3.0a cross-region sweep paragraph.

**Test scenarios.**
- A simulated IN run with top-3 categories carries 9 cross-region navs in F16 baseline log (3 categories x 3 regions).
- The `cross_country` sub-score in the digest's `winning_signals.cross_country` reaches >=1 on at least one top-3 category.
- When Meta Ad Library's cross-region query returns no ads (e.g., category has no US/UK presence), the sub-score falls back to 0 with `evidence_urls: []` and the F16 baseline records `cross_region_zero_return_for: <region>` in `data_quality_note`.
- Covers AE1.

**Verification.** Read `meta-top-digital-researcher.md` and confirm "MANDATORY" wording + sub-cap <=6. Read `meta-top-digital/SKILL.md` source-ladder section and confirm MANDATORY wording. Mirror sync per R6.

---

### U2. Rebalance tier-0 sub-budget within <=13 cap (R2)

**Goal.** Absorb U1's mandatory cross-region sweep within the existing <=13 nav cap by reducing category-level, dropping marketplace-level + open-ended sub-routes, and reducing retry reserve.

**Requirements.** R2.

**Files.**
- `meta-top-digital/references/agents/meta-top-digital-researcher.md` - Step 3.5 sub-cap allocation table

**Approach.**
- Edit Step 3.5 sub-cap allocation table per R2: category-level <=5 -> <=3, marketplace-level <=4 -> 0, open-ended <=2 -> 0, cross-region 0 -> <=9, retry <=2 -> <=1. Math: 3 + 9 + 1 = 13. Honors v1.9 KTD2 unconditional <=13 invariant.
- Edit sub-cap priority rule: cross-region sweep MUST fire on top-3 before retry can claim any nav. Encoded as a deterministic ordering check in the dispatch pseudocode.
- Update F16 baseline log's `data_quality_note` annotation template to reflect the new sub-route outcomes (per-sub-route skipped / succeeded counts).

**Patterns to follow.** v1.9 KTD2 sub-cap allocation table; v1.9.1 KTD1/KTD2/KTD3/KTD4/KTD5 rationale; existing priority rule in v1.8 Step 3.0a.

**Test scenarios.**
- Total tier-0 nav count in a simulated IN run stays <=13 with R1 active. Covers AE6.
- When Playwright MCP is unavailable, total nav count drops to 0 (tier-0 disabled) without budget overrun; sub-route failures fall through to tier-1 (WebSearch) per v1.9 fail-soft.
- F16 baseline log records per-sub-route skip / succeed counts in `data_quality_note` (e.g., `cross_region: 9/9 succeeded`, `category: 3/3 succeeded`).

**Verification.** Read `meta-top-digital-researcher.md` Step 3.5 sub-cap allocation table and confirm <=3 category + <=9 cross-region + <=1 retry = <=13. Mirror sync per R4.

---

### U3. Brief surface gloss for score/band/confidence relationship (R3)

**Goal.** Make the "Score 5/14 - skip" + "Confidence 90% - winning-grade" surface no longer read as contradictory.

**Requirements.** R3.

**Files.**
- `meta-top-digital/SKILL.md` - per-category rubric rendering block + verdict callout rendering

**Approach.**
- Add a one-line gloss (per KTD7) to the per-category rubric line, rendered immediately after the score-band: ` - score measures ad-inventory strength; confidence measures defensibility of the winner choice.`
- Add a conditional gloss to the verdict callout: when the verdict callout's confidence band is "winning-grade" but the winning category's score is in the "skip" band, append a single explanatory clause: ` (score 5/14 is thin-field - see per-category rubric for sub-scores)`.
- The gloss wording is a literal string; no dynamic computation beyond the existing score/band/confidence fields.

**Patterns to follow.** Prose-economy convention (one-line gloss; KTD7 above establishes the rule for v1.9.1); existing verdict callout rendering at v1.6 lines in the live SKILL.md.

**Test scenarios.**
- A simulated IN run with the v1.9.1 brief output renders the per-category rubric gloss on every category.
- When the verdict callout names a category with band "skip" + confidence "winning-grade", the conditional gloss appends.
- Covers AE5.

**Verification.** Read `meta-top-digital/SKILL.md` rubric rendering block + verdict callout rendering block and confirm gloss strings present. Mirror sync per R4.

---

## Verification Contract

Per-unit Verification is listed inline under each unit. Plan-level verification:

- Run a simulated `/meta-top-digital in` invocation against the live skill. Confirm:
  - The cross-region sweep navigates 9 times (3 categories x 3 regions) in tier-0.
  - Total tier-0 navs <=13.
  - F16 baseline log records the run with the v1.9.1 sub-route outcomes.
  - The `cross_country` sub-score lifts on at least one top-3 category. Covers AE1, AE4, AE6.
  - tier-0 completes within <=120s wall-clock time. Covers AE7.
- Inspect the rendered brief's per-category rubric line + verdict callout. Confirm the gloss strings render. Covers AE5.
- Mirror sync: `cp -f` from live to working copy + `diff -q` confirms parity. Per R4 and the `meta-top-skill-file-paths` memory rule.

## Definition of Done

A v1.9.1 brief from a fresh `/meta-top-digital in` invocation:
1. Reaches at least 7/14 on the spreadsheet winning category (AE4).
2. Carries the score/band/confidence gloss under Section (b) and the verdict callout (AE5).
3. Records per-sub-route outcomes in F16 baseline + `data_quality_note`.
4. Stays within <=13 tier-0 navs and <=120s latency budget (AE6, AE7).
5. Mirror parity byte-for-byte between live and working-copy paths (R6).

Global completion criteria:
- All five implementation units have `cp -f` mirror sync verified.
- F16 baseline log entry written per invocation.
- Brief output reads as one voice (prose-economy discipline per KTD7).
- No `category-pricing-research-required` hard-block callout fires spuriously on a run with >=1 observed_live category.

## Sources & Research

- **v1.9 plan**: `docs/plans/2026-10-01-001-feat-meta-top-skills-v19-comprehensive-research-plan.md` - KTD1 (cap-raise trigger), KTD2 (<=13 unconditional cap), KTD3 (<=120s latency budget, runtime-budget decision per v1.9 KTD7), KTD8 (both-skills-bump version invariant; mirror parity is the working-copy-vs-live-path discipline per the `meta-top-skill-file-paths` memory rule, not a v1.9 KTD).
- **v1.8 plan**: `docs/plans/2026-09-29-feat-meta-top-digital-v18-playwright-primary-plan.md` - KD3 (open-ended discovery via search-engine Playwright; degrades to tier-1 WebSearch under block).
- **v1.7 plan**: `docs/plans/2026-09-29-feat-meta-top-digital-v17-realtime-tier4-fix-plan.md` - Step 3.5 N=3 fire-with-cap-4 path; cache scope (tier-1/tier-2 only).
- **v1.6 plan**: `docs/plans/2026-09-29-1530-feat-meta-top-digital-v16-winning-verdict-plan.md` - 4-gate tie-break, R4 confidence formula, R3 skip rule.
- **v1.5 plan**: `docs/plans/2026-09-29-meta-top-digital-v15-improvements.md` - R-section on cross-region sweep (<=3 per category, observed-advertiser-overlap scoring); per-category hard-block. (Engagement and pain-signal extraction sections remain references for v1.9.2 redesign.)
- **Live SKILL.md and researcher specs**: `meta-top-digital/SKILL.md`, `meta-top-digital/references/agents/meta-top-digital-researcher.md`.
- **Live F16 baseline log**: `meta-top-digital/references/f16-baseline-log.md` (3 IN invocations logged; observed failure mode for tier-1 WebSearch = 0 results across 4 queries).
- **`meta-top-skill-file-paths` memory**: `meta-top-skill-file-paths.md` - every unit's verification ends with live-path grep + `cp -f` mirror sync.
- **`meta-top-digital-full-research-default` memory**: `meta-top-digital-full-research-default.md` - v1.9 KTD1 closes the spec/memory drift; v1.9.1 inherits the wider trigger.
