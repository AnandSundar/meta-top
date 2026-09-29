---
title: meta-top-digital v1.6 Winning Product Verdict - Plan
type: feat
date: 2026-09-29
artifact_contract: ce-unified-plan/v1
product_contract_source: ce-plan-bootstrap
execution: code
---

## Goal Capsule

**Objective.** A `/meta-top-digital <region>` invocation explicitly names a single winning digital-template product per region, with a deterministic tie-break rule and a 0-100 confidence percentage the user can read at a glance.

**Means.** Add a winning-product verdict callout under Section (b); make tier-0 (Meta Ad Library Playwright per-category nav) the default for top-3 categories; raise tier-4 Playwright cap from ≤2 to ≤4 when 1-2 of 3 top categories still lack `observed_live` after tier-3. (KTD1, KTD2, KTD3)

**Authority hierarchy.** Skill contract > SKILL.md > `meta-top-digital-researcher.md` > region YAML > working-copy mirror. Live paths under `~/.claude/skills/` are authoritative; `projects/meta-top/skills/` is mirror-only.

**Stop conditions.** Any unit failing its test scenarios blocks subsequent units. Total Playwright nav budget ≤9 per invocation (≤5 tier-0 + ≤4 tier-4) is hard — never exceeded.

**Execution profile.** Inline edits to live paths under `C:\Users\HP\.claude\skills\meta-top-digital\`, mirror via `cp -f` + `diff -q` to `projects/meta-top/skills/`, then commit + push to origin/main. ce-code-review is optional — additive scope does not warrant its load.

## Product Contract

### Summary

The v1.5 skill (shipped 2026-09-29, commit 9c8ea6a) renders Section (b) with per-category scores and `[unverified starting points, not observed-live]` caveats, but never names a single winning product. The `/meta-top-digital in` invocation this run scored 6/14 on three of five categories with `cross_country: 0` because tier-0 (Meta Ad Library Playwright) was optional and the tier-4 cap was conservative at ≤2. v1.6 closes both gaps: a deterministic verdict callout, mandatory tier-0, and a conditional tier-4 cap raise.

### Problem Frame

The v1.5 brief answers "what categories are selling?" but not "what should I build?". A user who runs `/meta-top-digital in` to find a winning product must eyeball Section (b), apply their own tie-break, and infer confidence. Three structural gaps prevent the skill from naming a winner:

1. **No verdict.** Section (b) ends with a category-level score list; no callout says "X is the winner". The user does the work the skill should do.
2. **Dead `cross_country` sub-score.** v1.5 added tier-0 (Meta Ad Library Playwright) with cap ≤5 but framed it as "mandatory for longevity/variants/cross_country" without enforcing it. The IN run shipped without firing tier-0, so `cross_country: 0` and `variants: 1` capped three sub-scores at the seed-anchor floor.
3. **Conservative tier-4 cap.** v1.5's tier-4 cap of ≤2 stops Playwright fallback after two navigations. On thin-data regions (IN, AE) where 1-2 of 3 categories lack observed_live after tier-3, two navs is insufficient — the brief ships with caveats that block user action.

v1.5's anti-fabrication hard-block (4-value `pricing_tier_source` enum, per-category observation requirement) is preserved unchanged — v1.6 is additive, not a relaxation.

### Requirements

R1. The skill MUST render a `🏆 Winning product (<region>): <category> · Score <X>/14 · Confidence <Y>%` callout under Section (b) on every invocation where at least one top-3 category carries `pricing_tier_source: observed_live`.
R2. The winning-product tie-break MUST be deterministic and ordered: (1) highest `winning_score.total`, (2) ≥1 `observed_live` example, (3) not in `prohibited_categories_digital`, (4) earliest YAML seed order. The callout names the category that wins all four gates; ties are broken by seed order.
R3. When 0 of 3 top categories carry `observed_live`, the skill MUST NOT render a winning verdict callout; the existing v1.5 hard-block callout (`category-pricing-research-required`) is the output and the brief ends.
R4. The confidence percentage MUST be a deterministic function of `(observed_live_count × 30) + (total_sources × 5) + (recency_bonus × 10)` capped at 100, where `recency_bonus = 1` when the live research ran within 24 hours of invocation. Thresholds: ≥70% = winning-grade, 40-69% = promising, <40% = speculative.
R5. Tier-0 (Meta Ad Library Playwright per-category nav) MUST fire by default on the top-3 categories from the region's `digital_categories` list. The cap of ≤5 navigations per invocation is preserved.
R6. Tier-0 MUST fall through to tier-1 (WebSearch) without user intervention when Playwright is unavailable, when Meta serves a verification wall (login/CAPTCHA), or when the Meta library rate-limits. The fall-through MUST append a one-line `data_quality_note` of the form `tier-0 (Meta Ad Library Playwright) skipped: <reason>; cross_country sub-score 0/2`.
R7. Tier-4 (Playwright browser fallback) cap MUST remain ≤2 by default. The cap MUST raise to ≤4 when, after tier-3 completes, 1 or 2 of the top-3 categories still lack any `observed_live` example. The raise is conditional on this gate, not opt-in.
R8. The total Playwright nav budget per invocation MUST remain ≤9 (≤5 tier-0 + ≤4 tier-4). When the tier-4 cap is raised, the data_quality_note MUST record `tier-4 cap raised: 2 → 4 (N of 3 categories still lack observed_live)`.
R9. The mirror under `projects/meta-top/skills/` MUST remain in sync with `~/.claude/skills/` after every edit batch, verified by `diff -q`. Out-of-sync state at commit time is a blocker.
R10. v1.5's anti-fabrication hard-block, source ladder, per-citation audit metadata, source-tier diversification cap (≥70% primary), and 5-column pricing table MUST remain unchanged. v1.6 is additive — no edits to those sections.

### Success Criteria

- Running `/meta-top-digital in` after v1.6 ships produces an explicit `🏆 Winning product (IN): <category> · Score X/14 · Confidence Y%` callout under Section (b) when at least one top-3 category carries `observed_live`.
- `cross_country: 2` (max) appears on at least one top-3 category per invocation, replacing the v1.5 baseline of `cross_country: 0`.
- A `/meta-top-digital <region>` invocation where 1-2 of 3 categories lack `observed_live` after tier-3 uses 3-4 Playwright navigations for tier-4 (vs. v1.5's 1-2), capped at 4.
- Total Playwright nav count per invocation does not exceed 9.
- `projects/meta-top/skills/` mirror matches `~/.claude/skills/` byte-for-byte after the v1.6 commit lands.

### Scope Boundaries

**In scope.** Three additive changes to meta-top-digital only:
- Winning verdict callout under Section (b) (U1)
- Tier-0 default behavior (U2)
- Tier-4 conditional cap raise (U3)

**Out of scope (deferred to v1.7+).**
- Multi-region correlation sub-score (idea 6 — requires U5 mirror units to be shipped first)
- Buyer-intent signals tier-2.5 (idea 5 — requires Reddit/Quora scraping infra)
- `volume_proxy` sub-score (idea 7 — requires Gumroad API integration)
- Confidence rubric rebalance (sub-score maxes stay at 14)

**Outside this product's identity.**
- meta-top (parent skill) does not get the verdict/tier-0/tier-4 changes. meta-top ships physical-product categories and a different tier-4 ladder. Bringing those changes into meta-top is a separate planning effort.
- HTML brief rendering (`--emit=html`) is unchanged.

### Dependencies

- v1.5 plan (`docs/plans/2026-09-29-meta-top-digital-v15-improvements.md`) is committed (9c8ea6a) and serves as the additive baseline.
- Playwright MCP server must be configured in the host environment for U2 and U3 to take effect. If unavailable, tier-0 and tier-4 fall through to their existing fallbacks (tier-1 WebSearch for tier-0; tier-5 curated anchors for tier-4).
- Region YAML at `references/regions/<region>.yaml` continues to authoritatively define `digital_categories`, `prohibited_categories_digital`, and `digital_marketplaces`.

### Open Questions

None. All three ideas were selected by the user from a menu in chat.

## Planning Contract

### Key Technical Decisions

**KTD1. Winning verdict tie-break is deterministic and four-gate.**
`session-settled: user-approved` — the user selected the recommended option (idea 1) from a ranked list surfaced in chat. The tie-break is a fixed ordering: highest score → ≥1 observed_live → not prohibited → earliest YAML seed order. No LLM judgment in the verdict — the same input produces the same winner.
*Governs R1, R2, R3.*

**KTD2. Tier-0 is the default for top-3 categories.**
`session-settled: user-approved` — the user selected the recommended option (idea 3). v1.5 framed tier-0 as "mandatory for longevity/variants/cross_country" but did not enforce it; the v1.5 IN run shipped without firing tier-0. v1.6 makes tier-0 unconditional in Step 3.0 of the ladder, with fall-through to tier-1 only when Playwright is unavailable or rate-limited.
*Governs R5, R6, R10.*

**KTD3. Tier-4 cap raises conditionally to ≤4.**
`session-settled: user-approved` — the user selected the recommended option (idea 4). The raise fires when 1-2 of 3 top categories still lack `observed_live` after tier-3, bounded by total Playwright budget ≤9 (≤5 tier-0 + ≤4 tier-4). The raise is not opt-in — the skill computes the gate state automatically.
*Governs R7, R8, R10.*

### Assumptions

1. The user wants a single winning product named, not a ranked list. (Inferred from "this slash command does not tell me what is the winning product".)
2. v1.5's anti-fabrication hard-block remains the failure mode the skill guards against. v1.6 is additive — relaxing the hard-block would require a separate planning effort and user authorization.
3. Playwright MCP server is configured in the host environment. If not, U2 and U3 degrade to v1.5 behavior (tier-0 fires only when explicitly called; tier-4 cap stays at ≤2).
4. The confidence formula `(observed_live_count × 30) + (total_sources × 5) + (recency_bonus × 10)` produces thresholds (≥70 / 40-69 / <40) that map cleanly to the existing `low` / `medium` / `high` bands. If a future run produces confidence percentages that compress to one band, the formula needs recalibration — recorded as future work, not a v1.6 scope.
5. `projects/meta-top/skills/` mirror is checked via `diff -q` after each edit batch. Manual byte-comparison is not part of v1.6 scope.

### Sequencing

U1, U2, U3 are independent edits to the same two files. Implementation order does not affect correctness, but the verification flow is: U1 first (simplest, highest user-visible impact), then U2 (touches more code paths), then U3 (conditional logic depends on U2's tier-0 output).

## Implementation Units

### U1. Winning Product Verdict Callout

**Goal.** Add a deterministic winning-product verdict callout under Section (b) of `meta-top-digital/SKILL.md`. The callout names a single category per region with a score and a 0-100 confidence percentage.

**Requirements.** R1, R2, R3, R4.

**Files.**
- `C:\Users\HP\.claude\skills\meta-top-digital\SKILL.md` — add the verdict rendering under Section (b); update the v1.5 banner to v1.6 with a one-line changelog
- `C:\Users\HP\projects\meta-top\skills\meta-top-digital\SKILL.md` — mirror after live edit

**Approach.**
1. Add a `### Winning Product Verdict` subsection under Section (b) that reads from the JSON digest's `top_categories[0..2]` and `pricing_examples[]`.
2. The verdict function applies the four-gate tie-break (KTD1):
   - Filter to top-3 from YAML `digital_categories` order
   - Sort by `winning_score.total` descending, then YAML seed order ascending
   - First category meeting all four gates (highest score → ≥1 observed_live → not prohibited → earliest seed order) is the winner
   - If no category meets gate 2 (≥1 observed_live), no verdict is rendered — the v1.5 hard-block callout is the output
3. The confidence percentage is computed as `(observed_live_count × 30) + (total_sources × 5) + (recency_bonus × 10)` where `recency_bonus = 1` when the research ran within 24 hours, else 0. Capped at 100.
4. Render format: `🏆 Winning product (<region>): <category> · Score <X>/14 · Confidence <Y>%` followed by a one-line reason citing the tie-break inputs.
5. Update the v1.5 banner line to v1.6 with: `v1.6 (2026-09-29) adds a deterministic winning-product verdict callout under Section (b) (4-gate tie-break, 0-100 confidence), makes tier-0 (Meta Ad Library Playwright) the default for top-3 categories, and raises tier-4 cap conditionally from ≤2 to ≤4 when 1-2 of 3 categories still lack observed_live after tier-3. v1.5 anti-fabrication hard-block, source ladder, and 5-column pricing table are unchanged.`

**Test Scenarios.**
- Happy path: All 3 top categories have observed_live, category A scores 12, category B scores 11, category C scores 9 → callout reads `🏆 Winning product (IN): <A> · Score 12/14 · Confidence 85%`. B and C are not in the callout.
- Caveats path: 1 of 3 has observed_live (category B at 11) → callout names B with confidence ≤60%.
- Hard-block path: 0 of 3 has observed_live → no verdict callout rendered; v1.5 hard-block callout is the output.
- Prohibited path: highest-scoring category (14/14) is in `prohibited_categories_digital` (e.g., `saas-subscriptions`) → verdict falls to the next-eligible category; callout does not name the prohibited one.
- Tie-score path: category A and B both score 11 with observed_live → A wins by YAML seed order (lower index = earlier in `digital_categories` list).
- Recency bonus: research ran within 24h → confidence = observed_live × 30 + total_sources × 5 + 10; >24h → no bonus.

**Verification.** Run `/meta-top-digital in` against the live skill; verify the callout appears (or hard-block callout replaces it) under Section (b). Recompute confidence by hand and check it matches the rendered value.

### U2. Tier-0 Default Behavior

**Goal.** Make tier-0 (Meta Ad Library Playwright per-category nav) the default for top-3 categories. The v1.5 ladder framed tier-0 as mandatory for ad-inventory sub-scores but did not enforce firing.

**Requirements.** R5, R6, R10.

**Files.**
- `C:\Users\HP\.claude\skills\meta-top-digital\SKILL.md` — update the Step 3.0 ladder description to make tier-0 unconditional
- `C:\Users\HP\.claude\skills\meta-top-digital\references\agents\meta-top-digital-researcher.md` — update Step 3.0 sub-agent instructions to fire tier-0 by default
- `C:\Users\HP\projects\meta-top\skills\meta-top-digital\SKILL.md` — mirror
- `C:\Users\HP\projects\meta-top\skills\meta-top-digital\references\agents\meta-top-digital-researcher.md` — mirror

**Approach.**
1. In `meta-top-digital/SKILL.md` Step 3.0, change "Tier-0 (v1.5+, per-category mandatory)" to "Tier-0 (v1.6+, per-category default)" and add: "Fires on every top-3 category by default; falls through to tier-1 only when Playwright is unavailable, when Meta serves a verification wall, or when Meta rate-limits the per-region query. The fall-through appends a one-line `data_quality_note`."
2. In `meta-top-digital-researcher.md` Step 3.0, add a Step 3.0.0 block that runs before the existing Step 3.0 sub-score routing: "For each top-3 category, attempt `browser_navigate` to `https://www.facebook.com/ads/library/?active_status=active&country={region}&q={category-keyword}`. If the page renders an ad grid (a11y tree shows ≥1 ad card), extract longevity/variants/cross_country sub-scores. If the page returns a verification wall, CAPTCHA, or empty grid, append `tier-0 skipped for {category}: {reason}` to `data_quality_note` and set `cross_country: 0/2`, `variants: 0/2`, `longevity: 1/2` (the seed floor) for that category."
3. Cap ≤5 Playwright navs for tier-0 remains unchanged. Tier-4 ≤2 stays in this unit; U3 raises it.
4. Do NOT change the total Playwright budget wording here — U3's wording supersedes it.

**Test Scenarios.**
- Happy path: `/meta-top-digital in` fires Playwright on Meta Ad Library for each of top-3 categories; ≥1 ad grid renders per category; sub-scores populated.
- Cap respected: tier-0 uses ≤5 navs even with 3 top-3 categories fired (3 navs is the typical case; cap allows 5).
- Fallback (verification wall): Meta serves login/CAPTCHA → tier-0 skipped with `data_quality_note`; tier-1 WebSearch fires; cross_country sub-score 0/2.
- Fallback (rate-limit): Meta returns empty grid → tier-0 skipped; sub-scores at seed floor.
- Fallback (Playwright unavailable): host has no Playwright MCP → tier-0 skipped with reason `playwright MCP not configured`; sub-scores at seed floor.

**Verification.** Run `/meta-top-digital in`; verify in the JSON digest that `data_quality_note` records tier-0 firings (or skip reasons) for each top-3 category, and that `winning_score.cross_country` is populated (≥1) rather than 0.

### U3. Tier-4 Conditional Cap Raise

**Goal.** Raise tier-4 (Playwright browser fallback) cap from ≤2 to ≤4 when 1-2 of 3 top categories still lack `observed_live` after tier-3 completes.

**Requirements.** R7, R8, R10.

**Files.**
- `C:\Users\HP\.claude\skills\meta-top-digital\SKILL.md` — update the tier 4 ladder description; update the total Playwright budget line to ≤9
- `C:\Users\HP\.claude\skills\meta-top-digital\references\agents\meta-top-digital-researcher.md` — update tier-4 instructions to compute the raise gate
- `C:\Users\HP\projects\meta-top\skills\meta-top-digital\SKILL.md` — mirror
- `C:\Users\HP\projects\meta-top\skills\meta-top-digital\references\agents\meta-top-digital-researcher.md` — mirror

**Approach.**
1. In `meta-top-digital/SKILL.md` ladder section, replace "Cap at ≤2 browser navigations per invocation" with: "Default cap ≤2; raises to ≤4 when, after tier-3 completes, 1 or 2 of the top-3 categories still lack any `pricing_examples[].pricing_tier_source: observed_live`. The raise is automatic — the skill computes the gate state. Total Playwright nav budget ≤9 per invocation (≤5 tier-0 + ≤4 tier-4)."
2. In `meta-top-digital-researcher.md` ladder section, add a Step 3.5 check before tier-4 fires: "Compute `categories_lacking_observed_live = top_categories[0..2].filter(c => c.pricing_examples.length === 0 || !c.pricing_examples.some(p => p.pricing_tier_source === 'observed_live')).length`. If 1 ≤ N ≤ 2, set `tier_4_cap = 4` and append `tier-4 cap raised: 2 → 4 (N of 3 categories still lack observed_live)` to `data_quality_note`. Else, `tier_4_cap = 2`."
3. Update the "v1.5+ v1.5+ trigger rationale" note to reflect that the v1.4 "≥2 marketplace URLs" threshold is now superseded by the conditional raise.
4. Do NOT raise the tier-4 cap when 3 of 3 categories lack observed_live (brief BLOCKED before tier-4 fires; existing hard-block callout is the output).

**Test Scenarios.**
- Raise path: 1 of 3 categories lacks observed_live after tier-3 → tier-4 fires with cap 4; 2 navs used (cap is 4 but ≤4 means ≤4).
- Raise path: 2 of 3 categories lack observed_live → tier-4 cap = 4; used count recorded.
- No-raise path: 0 categories lack observed_live → tier-4 cap stays at ≤2.
- All-blocked path: 3 of 3 lack observed_live → tier-4 does NOT fire; v1.5 hard-block callout is the output; `data_quality_note` does NOT include the cap-raise note (brief blocked before tier-4).
- Cap respected: even with raise, total Playwright nav ≤9 (5 tier-0 + 4 tier-4).
- data_quality_note records the raise: `tier-4 cap raised: 2 → 4 (2 of 3 categories still lack observed_live)`.

**Verification.** Run `/meta-top-digital in` with the v1.6 skill; verify `data_quality_note` contains (or omits) the cap-raise note based on the post-tier-3 gate state. Verify total Playwright nav count via the tier counters in the JSON digest.

### U4. Mirror Sync

**Goal.** Sync `~/.claude/skills/meta-top-digital/` to `projects/meta-top/skills/meta-top-digital/` after U1-U3 edits land.

**Requirements.** R9.

**Files.**
- All 4 files edited in U1-U3.

**Approach.**
1. After U1, U2, U3 land on live paths under `C:\Users\HP\.claude\skills\`, run `cp -f` for each modified file from live → working-copy.
2. Verify with `diff -q` — silent (no diff output) means in-sync.
3. If `diff -q` produces output, the unit fails; re-run `cp -f` and re-verify.

**Test Scenarios.**
- Sync after U1: `diff -q` on SKILL.md produces no output.
- Sync after U2: `diff -q` on SKILL.md + researcher.md produces no output.
- Sync after U3: `diff -q` on SKILL.md + researcher.md produces no output.
- Out-of-sync detection: any `cp -f` that fails (read-only working copy, etc.) blocks the unit.

**Verification.** Run `diff -q` on each of the 4 modified file pairs; all silent = pass.

## Verification Contract

### Lint / Format / Build

None — this is a Markdown-skill edit, not code. No TypeScript, no Python, no test runner.

### Live Skill Smoke Test

After U1-U3 land:

1. Run `/meta-top-digital in` against the live v1.6 skill.
2. Verify:
   - Line 1 is the badge `📊 meta-top-digital v1.6 · region: in · 2026-09-29`.
   - The `Resolved` block is present.
   - Section (b) renders the 5-column pricing table (v1.5 preserved).
   - Either a `🏆 Winning product (IN):` callout OR the v1.5 `category-pricing-research-required` callout is present (mutually exclusive).
   - `data_quality_note` records tier-0 firings (or skip reasons) for each top-3 category.
   - `winning_score.cross_country` is populated (≥1) if tier-0 fired successfully.
3. Run `diff -q` on the 4 modified file pairs against the working-copy mirror. All silent = pass.

### Doc Review

Run `ce-doc-review` against this plan with `mode:non-interactive` before declaring the plan shippable.

### Behavior Preserved from v1.5

Verify these v1.5 behaviors are unchanged after the v1.6 edit:

- The 4-value `pricing_tier_source` enum (`observed_live | observed_snippet | inferred_seed | unverified`)
- The per-category hard-block (0 of 3 → blocked; 1-2 of 3 → ship with caveats; 3 of 3 → ship clean)
- The source ladder tiers 0-5 (only the conditions change)
- The source-tier diversification cap (≥70% primary, ≤30% secondary)
- The 5-column pricing table (Category | Price range | Tier source | Confidence | Evidence)
- The per-citation audit metadata (tier + extracted_fields + audit_provenance)
- The snapshot versioning fields (snapshot_version, snapshot_id, prior_snapshot_ref, price_delta[])

### Definition of Done

A unit is done when:
- All required file edits are committed to live paths under `C:\Users\HP\.claude\skills\`.
- The working-copy mirror matches byte-for-byte (`diff -q` silent).
- The unit's Test Scenarios pass on a `/meta-top-digital in` invocation.
- The unit's Verification step is satisfied.

The plan is done when:
- U1, U2, U3, U4 are all done.
- The live skill smoke test (Verification Contract) passes.
- `ce-doc-review` returns without P0/P1 findings (or all P0/P1 findings resolved).
- A single commit + push to origin/main lands the v1.6 changes; the commit message does NOT include the `🤖 Generated with [Claude Code]` footer.
