---
title: "Improve meta-top and meta-top-digital for comprehensive research and sharper winning-product detection"
type: feat
date: 2026-10-01
---

> **Path convention.** All paths in this plan are relative to the live skills root `C:\Users\HP\.claude\skills\` (what `/meta-top` and `/meta-top-digital` actually load). The working-copy mirror at `C:\Users\HP\projects\meta-top\skills\` is the version-controlled draft. **Every unit's verification ends with a live-path grep AND a `cp -f` mirror sync** — see each unit's Verification for the exact commands. Editing the working copy alone silently leaves the live skill at the prior version (per the `meta-top-skill-file-paths` memory rule).

## Summary

Bump both `/meta-top` and `/meta-top-digital` from v1.8 to v1.9 with three load-bearing changes: widen the Step 3.5 cap-raise trigger to the user's `meta-top-digital-full-research-default` memory rule's four-condition union (closing the spec/memory drift); drop the Step 3.5 conditional gate and make the tier-0 Playwright cap ≤13 unconditional, with the per-invocation latency budget raised to ≤120s; port the 🏆 winning-verdict callout from `meta-top-digital` to `meta-top`, closing the v1.6 KTD4 asymmetry. Sync the U5 mirror unit (US, CA, UK, AU, AE region YAMLs) from the working copy to the live path with per-region `prohibited_categories_digital` curation per the region's regulator. Sharpen weak signals (engagement, marketplace, pain_signal) is **deferred to v1.9.1** — its premise depends on data availability the user has not yet measured.

## Problem Frame

Both skills evolved v1.3 → v1.8 over a three-day window (2026-09-27 → 2026-09-29) and now ship a sophisticated tier-0 Playwright-primary ladder, a 6-signal winning-product rubric, a per-category observed-live pricing hard-block, and (in `meta-top-digital` only) a unified 🏆 verdict callout. Three load-bearing gaps remain.

First, the user's `meta-top-digital-full-research-default` memory rule (filed 2026-09-28 after a drill-in for IN spreadsheet templates) widens the Step 3.5 cap-raise trigger to fire on `partial_research: true`, `rate_limit_hit: true`, any `inferred_seed` pricing example, or any `confidence: low` signal — but the v1.8 spec only fires the trigger on `N∈{1,2,3} of top-3 categories still lack observed_live`. The v1.7 plan appendix explicitly deferred this widening as "future work". The user has been operating under the memory rule while the spec lags.

Second, the v1.6 plan made a deliberate decision-by-omission (KTD4) to ship the 🏆 verdict callout in `meta-top-digital` but not in `meta-top`, on the grounds that "meta-top ships physical-product categories and a different tier-4 ladder" and "bringing those changes into meta-top is a separate planning effort." That follow-up is the work this plan executes. With the v1.8 Playwright-primary ladder unifying the two skills' tier semantics, the port is now mechanical.

Third, `meta-top-digital` ships only India in v1; the U5 mirror unit for US / CA / UK / AU / AE was planned but not authored. The working copy at `C:\Users\HP\projects\meta-top\skills\meta-top-digital\references\regions\` already has all five mirror YAMLs authored — they have not been synced to the live path. Each call to a non-IN region emits the "Region not yet shipped" notice and stops, forcing the user to fall back to `/meta-top <region>` for non-IN digital-product research. U4's work is the live-path sync, not new authoring.

Two smaller gaps surface in this revision. The 6-signal rubric's `engagement`, `marketplace`, and `pain_signal` sub-scores are sourced from tier-1 WebSearch under the v1.8 Playwright-primary regime — but extracting them from Playwright-rendered snapshots depends on data availability the user has not yet measured. Most Meta Ad Library ads carry ≤5 comments per KTD5 of the v1.6 plan; without empirical validation, sharpening changes the source without changing informativeness. This work is deferred to v1.9.1. The v1.8 Q5 open question on latency budget raise needs empirical grounding; v1.9 ships the raise on user preference (the user explicitly asked for higher budgets) and tracks latency in F16 baseline log under `references/f16-baseline-log.md` per skill tree.

## Requirements

### Comprehensive research

- R1. `meta-top/references/agents/meta-top-researcher.md` Step 3.5 trigger widens to the four-condition union: `N∈{1,2,3} of top-3 categories still lack observed_live` OR `partial_research: true` OR `rate_limit_hit: true` OR any `pricing_examples[].pricing_tier_source: inferred_seed`. **Falsification test:** if post-cutover invocations under v1.8 narrower trigger produce briefs with ≥2 of 3 categories carrying `observed_live` in ≥80% of runs, the wider trigger is gratuitous and v1.9.1 reverts to the narrower form. R1's implementer documents the trigger-widening rationale in the changelog; v1.9.1 work re-reads the data before locking the trigger.
- R2. `meta-top-digital/references/agents/meta-top-digital-researcher.md` Step 3.5 trigger widens to the same four-condition union (matches meta-top wording).
- R3. The Step 3.5 conditional gate is removed. Tier-0 Playwright cap is **unconditional ≤13** in both researcher specs. Cap remains a hard ceiling — researcher cannot exceed ≤13 under any condition. Sub-cap allocation for meta-top-digital: ≤5 category-level + ≤4 marketplace-level + ≤2 open-ended = ≤11 default + 2 retry navs = ≤13 total. Sub-cap allocation for meta-top: ≤7 Meta Ad Library + ≤6 top_brands = ≤13 total.
- R4. `SKILL.md` (both skills) v1 ceiling raises from ≤90s to ≤120s per invocation. The `data_quality_note` template wording accommodates the wider range when a region exceeds the median.
- R5. F16 baseline logging added to each researcher spec. One ISO-8601 line per invocation to `references/f16-baseline-log.md` per skill tree. Schema: `<ISO8601> <region> <observed_live_lacking:0-3> <partial_research:0|1> <rate_limit_hit:0|1> <verification_wall_hit:0|1> <inferred_seed:0|1> <outcome:succeeded|partial|blocked> <latency_ms:integer>`. The log is for empirical validation of latency-budget raise (Q5); it does not gate any v1.9 work. Calibration work that uses this log is deferred to v1.9.1+ per the §Deferred for later section.

### Verdict callout parity

- R6. `meta-top/SKILL.md` Step 2 item 2 gains the 🏆 winning-verdict callout block (the v1.6 meta-top-digital wording at live SKILL.md lines 157-174, verbatim except where noted in KTD4).
- R7. `meta-top/SKILL.md` verdict callout references `prohibited_categories` (meta-top's actual key name, confirmed at live `meta-top/references/regions/us.yaml` line 13), NOT `prohibited_categories_digital`. Gate 3 wording is otherwise identical.
- R8. v1.6 verdict-skip rule (0 of 3 → no callout, hard-block callout is the output) ports verbatim; gate 1-4 tie-break order and the R4 confidence formula match digital.
- R9. `meta-top/SKILL.md` v1.9 changelog FYI blockquote renders once per invocation under Option B's trust + ethics blockquote: `> v1.9 — 🏆 winning-verdict callout now applies (parity with meta-top-digital since v1.6). Use the per-category rubric in Section (b) for the underlying scoring.` The blockquote is gated to first-render-after-cutover (one-shot; cleared after first invocation, or removed in v1.9.1).

### U5 mirror unit

- R10. `meta-top-digital/references/regions/us.yaml` is verified against the working-copy source at `C:\Users\HP\projects\meta-top\skills\meta-top-digital\references\regions\us.yaml`, structurally sound (same 14 top-level keys as `in.yaml`), and synced to the live path at `C:\Users\HP\.claude\skills\meta-top-digital\references\regions\us.yaml`.
- R11. Same verification + sync for `ca.yaml`, `uk.yaml`, `au.yaml`.
- R12. `ae.yaml` ships with a `last_reviewed: 2026-10-01` annotation and explicit "TBD / placeholder pending Arabic-language marketplace research" notes on any list where the implementer lacks confidence in the curation.
- R13. `meta-top-digital/SKILL.md` Pre-Flight "Region-mirror check" (line 108) updates to remove the "Region not yet shipped" stop; the Pre-Failure-Modes "Region not yet shipped (mirror landed later)" section (lines 283-306) is deleted or annotated as "applies only when a future v2 region ships ahead of its YAML".
- R14. Each of the five mirror YAMLs' `prohibited_categories_digital` lists are curated per the region's regulator (FTC for US, Ad Standards + CRTC for CA, ASA for UK, AANA for AU, NMC + TRA for UAE). India's list is the seed; per-region additions: US (FTC) → drop `forex-copy-trading`, add `crypto-token-presale-mechanics`; UK (ASA) → add `binary-options`, `trading-signal-services`; AU (AANA) → add `gambling-in-app-purchase`, `crypto-derivatives`; UAE (NMC + TRA) → add `forex-without-license`, `crypto-without-license`; CA (Ad Standards + CRTC) → mirror US with provincial health-claim nuances. The implementer consults each regulator's published guidance to author the additions; this is not a copy-paste from India's list.

## Key Technical Decisions

KTD1. Step 3.5 trigger widens to a four-condition union, with a falsification test baked into R1. Rationale: the user's memory rule has held this wider trigger since 2026-09-28; the v1.7 plan appendix explicitly deferred the spec widening as "future work". v1.9 closes the spec/memory drift. The falsification test (R1) is the empirical guard against the change being gratuitous — if ≥80% of v1.8 invocations already produced briefs with ≥2 of 3 categories carrying `observed_live`, the wider trigger adds nothing and v1.9.1 reverts. The test is a guard, not a blocking gate.

KTD2. The Step 3.5 conditional gate is removed; tier-0 Playwright cap is unconditional ≤13. Rationale: under the wider trigger (KTD1), the gate fires on essentially every invocation with non-trivial data — the conditional logic is dead. Removing it simplifies the researcher spec and matches the user's preference for more comprehensive research. Sub-cap allocation: meta-top-digital gets ≤5 category-level + ≤4 marketplace-level + ≤2 open-ended = ≤11 default + 2 retry navs; meta-top gets ≤7 Meta Ad Library + ≤6 top_brands. Cap is a hard ceiling.

KTD3. Per-invocation latency budget raises from ≤90s to ≤120s. Rationale: the user explicitly asked for higher latency budgets; 13 navs × ~7s/nav worst case + overhead = ≤120s. **This is a runtime-budget decision, not a calibration parameter** — it affects invocation completion, not output reliability. Per-invocation latency is logged to F16 baseline for empirical validation; if post-cutover median exceeds 75s, the cap-raise gate tightens to ≤11 navs in v1.9.1 (per Q5).

KTD4. Verdict callout ports to `meta-top` with gate 3 wording adapted. Rationale: meta-top uses `prohibited_categories` (confirmed at live `meta-top/references/regions/us.yaml` line 13), digital uses `prohibited_categories_digital` (confirmed at live `meta-top-digital/references/regions/in.yaml` line 13). With the v1.8 Playwright-primary ladder unifying the two skills' tier semantics, the port is mechanical. **The implementer MUST diff the two lists per region** to identify any categories that appear in only one list — if scope divergence exists, gate 3 wording must include a scope qualifier (`for physical products` / `for digital products`).

KTD5. U5 mirror unit's `digital_marketplaces` and `digital_categories` lists per region mirror `in.yaml`'s structure exactly (per-region variation lives only in the values: currency, languages, regulatory body, the regional suffix on global marketplaces). The implementer does not vary list membership beyond regional suffix additions — this is a structural port, not a per-market discovery effort. AE.yaml is split off (U4b) given unique regulatory + Arabic-language constraints.

KTD6. U5 mirror sync is a working-copy-to-live copy (`cp -f` + `diff -q`), not a re-authoring. The working copy at `C:\Users\HP\projects\meta-top\skills\meta-top-digital\references\regions\` already has all 5 mirror YAMLs (confirmed via `ls`); U4's work is verification + sync. The per-region `prohibited_categories_digital` curation in R10-R14 is the only authoring work in U4.

KTD7. Latency-budget raise and calibration deferral apply different epistemic standards. **Latency-budget is a runtime-budget decision (user preference overrides empirical gating because latency affects invocation completion, not output reliability).** **Calibration (confidence formula, hard-block threshold) is a signal-confidence parameter (measurement-driven because getting it wrong affects output reliability).** v1.9 ships the latency raise on user preference; v1.9.1+ ships calibration only after F16 baseline data validates the change.

KTD8. Both skills bump from v1.8 to v1.9. Rationale: the changes cross the breaking/non-breaking boundary for `meta-top` (verdict callout is new output) but stay non-breaking for `meta-top-digital` (the user has been operating under the memory rule already). Bumping both keeps the skills on a version curve close to synchronized; future versions may diverge independently when one skill needs a feature the other doesn't. The SKILL CONTRACT bullet 1 wording in each skill is updated.

## Implementation Units

### U1. Widen Step 3.5 trigger, drop conditional gate, raise default cap, add F16 logging (both skills)

**Goal.** Close the spec/memory drift on the cap-raise trigger. Drop the Step 3.5 conditional gate (the wider trigger makes it vestigial). Raise tier-0 Playwright cap to unconditional ≤13. Add F16 baseline logging for empirical validation of latency-budget raise.

**Requirements.** R1, R2, R3, R4, R5.

**Dependencies.** None — first unit. Subsequent units consume the new cap math.

**Files.**
- `meta-top/references/agents/meta-top-researcher.md`
- `meta-top/SKILL.md`
- `meta-top/references/f16-baseline-log.md` (new)
- `meta-top-digital/references/agents/meta-top-digital-researcher.md`
- `meta-top-digital/SKILL.md`
- `meta-top-digital/references/f16-baseline-log.md` (new)

**Approach.**
- Rewrite each researcher spec's Step 3.5 pseudocode: when ANY of the four trigger conditions (KTD1) fires, set `tier_0_cap = 13`. When none fires, also set `tier_0_cap = 13` (unconditional per KTD2). The conditional gate's `N == 0 → cap = 9` branch is removed; the `N in (1, 2, 3) → cap = 13` branch is kept as a vestigial alias for the legacy case.
- Apply sub-cap allocations per KTD2: meta-top-digital ≤5 cat + ≤4 mkt + ≤2 open-ended; meta-top ≤7 Meta Ad Library + ≤6 top_brands.
- Update each SKILL.md's v1 ceiling wording from ≤90s to ≤120s; adjust `data_quality_note` template.
- Append F16 baseline logging as a new step in each researcher spec. One ISO-8601 line per invocation to the new `references/f16-baseline-log.md` per skill tree. Schema per R5.
- Bump SKILL CONTRACT bullet 1 wording in both SKILL.md files: "currently v1.9, bumped from v1.8 in this revision". v1.9 (2026-10-01) entry summarises: trigger widened, conditional gate dropped, default cap ≤13, latency budget ≤120s, F16 logging started.

**Patterns to follow.** Step 3.5 pseudocode at live `meta-top-digital-researcher.md` lines 162-181 and `meta-top-researcher.md` lines 141-166; v1.7 plan appendix's deferred-widening note; the `meta-top-digital-full-research-default` memory rule.

**Test scenarios.**
- Step 3.5 trigger fires on `partial_research: true` even with 0 of 3 categories lacking `observed_live`. Covers AE1.
- Step 3.5 trigger fires on `rate_limit_hit: true` even with 0 of 3 categories lacking `observed_live`. Covers AE2.
- Cap stays hard at ≤13 — no nav-count explosion when all four conditions fire.
- An F16 baseline log line is written per invocation with the R5 schema.
- Sub-cap allocation respects per-route ceilings (≤5 cat, ≤4 mkt, ≤2 open-ended for digital; ≤7 Meta Ad Library, ≤6 top_brands for meta-top).

**Verification.**
- Run `scripts/test_keyless_search.py` to confirm scripts/ parity preserved.
- Grep the live path: `grep "v1.9" "C:/Users/HP/.claude/skills/meta-top/SKILL.md"` and `grep "v1.9" "C:/Users/HP/.claude/skills/meta-top-digital/SKILL.md"` — confirm version bump.
- Mirror sync: `cp -f "C:/Users/HP/.claude/skills/meta-top/references/agents/meta-top-researcher.md" "C:/Users/HP/projects/meta-top/skills/meta-top/references/agents/"` and `diff -q` to confirm working-copy parity. Repeat for `meta-top-digital`.
- Read `references/f16-baseline-log.md` after a test invocation — confirm a new line was written with the R5 schema.

---

### U2. Port winning-verdict callout to meta-top + v1.9 changelog FYI (meta-top only)

**Goal.** Close the v1.6 KTD4 asymmetry. Port the 🏆 verdict callout to `meta-top` with gate 3 wording adapted. Add the v1.9 changelog FYI blockquote so first-time users understand the new affordance.

**Requirements.** R6, R7, R8, R9.

**Dependencies.** U1 — needs updated cap math and latency budget reflected in SKILL.md before the verdict callout sits next to them.

**Files.**
- `meta-top/SKILL.md`

**Approach.**
- Port the entire v1.6 winning-product verdict block (live `meta-top-digital/SKILL.md` lines 157-174) to `meta-top/SKILL.md` under Step 2 item 2, immediately after the per-category rubric lines.
- Adapt gate 3: replace "Category name NOT in `prohibited_categories_digital`" with "Category name NOT in `prohibited_categories`".
- Otherwise keep the callout format, four-gate tie-break order, R4 confidence formula, R3 skip rule, and R6 band thresholds verbatim.
- **Diff step (KTD4):** before finalising the port, the implementer diffs `meta-top/references/regions/in.yaml`'s `prohibited_categories` against `meta-top-digital/references/regions/in.yaml`'s `prohibited_categories_digital`. If a category appears in only one list, gate 3 wording must include a scope qualifier (`for physical products` / `for digital products`). Document the diff in the v1.9 changelog.
- Add the v1.9 changelog FYI blockquote per R9, gated to first-render-after-cutover. The blockquote sits under Option B's trust + ethics blockquote.
- Bump the v1.9 entry in SKILL CONTRACT bullet 1 to note the verdict callout ports in meta-top.

**Patterns to follow.** Live `meta-top-digital/SKILL.md` lines 157-174 (verdict callout), 196-204 (Option B trust + ethics blockquote); v1.6 plan (`docs/plans/2026-09-29-1530-feat-meta-top-digital-v16-winning-verdict-plan.md`).

**Test scenarios.**
- A fresh `/meta-top in` invocation produces a 🏆 callout naming a category, the `winning_score.total`, and a confidence percentage. Covers AE3.
- The callout uses `prohibited_categories` (not `prohibited_categories_digital`) — verify by reading the rendered output. If the KTD4 diff step identifies scope divergence, the qualifier renders.
- When 0 of 3 categories carry `observed_live`, the verdict callout is suppressed and the v1.5 hard-block callout is the output. Covers AE4.
- The four-gate tie-break is deterministic — same digest input produces same winner.
- The confidence percentage renders with band suffix `winning-grade` / `promising` / `speculative` per R6 thresholds.
- First invocation after U2 ships renders the v1.9 changelog FYI blockquote under Option B; subsequent invocations do not.

**Verification.**
- Invoke `/meta-top in` against a known digest shape — confirm the callout renders with correct gate 3 wording, callout format, confidence percentage, and band suffix.
- Cross-check by invoking `/meta-top-digital in` with the same input — confirm structurally parallel output.
- Read `meta-top/SKILL.md` and confirm the v1.9 changelog FYI blockquote renders once (or is annotated to clear after first invocation).
- Grep the live path: `grep "v1.9" "C:/Users/HP/.claude/skills/meta-top/SKILL.md"` — confirm version bump.
- Mirror sync: `cp -f "C:/Users/HP/.claude/skills/meta-top/SKILL.md" "C:/Users/HP/projects/meta-top/skills/meta-top/SKILL.md"` and `diff -q` to confirm working-copy parity.

---

### U3. U5 mirror sync to live path (meta-top-digital only, non-AE regions)

**Goal.** Sync the US, CA, UK, AU region YAMLs from the working copy to the live path. Verify structural soundness. The working copy already has these YAMLs authored; U3's work is verification + sync, not authoring.

**Requirements.** R10, R11, R13.

**Dependencies.** U1 — needs the updated cap math and latency budget reflected in SKILL.md before the Pre-Flight update lands.

**Files.**
- `meta-top-digital/SKILL.md`
- `meta-top-digital/references/regions/us.yaml` (live-path sync; authored in working copy)
- `meta-top-digital/references/regions/ca.yaml` (live-path sync)
- `meta-top-digital/references/regions/uk.yaml` (live-path sync)
- `meta-top-digital/references/regions/au.yaml` (live-path sync)

**Approach.**
- For each of the four regions, verify the working-copy YAML structurally matches `in.yaml` (same 14 top-level keys, list-of-dicts shape for `digital_categories` and `digital_marketplaces`). If structure diverges, fix in working copy first, then sync.
- Sync each YAML from working copy to live path: `cp -f "C:/Users/HP/projects/meta-top/skills/meta-top-digital/references/regions/{region}.yaml" "C:/Users/HP/.claude/skills/meta-top-digital/references/regions/"`. Verify with `diff -q`.
- Curate each region's `prohibited_categories_digital` list per R10/R11 + KTD5: per-region additions (US drops `forex-copy-trading`, adds `crypto-token-presale-mechanics`; CA mirrors US with provincial health-claim nuances; UK adds `binary-options`, `trading-signal-services`; AU adds `gambling-in-app-purchase`, `crypto-derivatives`). The implementer consults each regulator's published guidance to author additions.
- Update `meta-top-digital/SKILL.md` Pre-Flight "Region-mirror check" (line 108): remove the "Region not yet shipped" stop. Update Pre-Failure-Modes "Region not yet shipped (mirror landed later)" section (lines 283-306): either delete or annotate as "applies only when a future v2 region ships ahead of its YAML".
- Bump the v1.9 entry in SKILL CONTRACT bullet 1 to note U5 mirror lands (3 regions shipping this unit).

**Patterns to to follow.** Working-copy YAMLs at `C:\Users\HP\projects\meta-top\skills\meta-top-digital\references\regions\{us,ca,uk,au}.yaml` (already authored); live `meta-top-digital/SKILL.md` Step 2 region-mirror check; v1.6 plan's mirror-sync discipline.

**Test scenarios.**
- `/meta-top-digital us` invokes without the "Region not yet shipped" notice and returns a real six-section brief. Covers AE6.
- `/meta-top-digital ca`, `/meta-top-digital uk`, `/meta-top-digital au` similarly each invoke and return real briefs.
- Each region's YAML validates against the same parser expectations as `in.yaml` (top-level keys, sub-key shape, list-of-dicts).
- The per-region `prohibited_categories_digital` filter applies correctly — at least one region-specific category is added vs India's list, and is filtered from live research.

**Verification.**
- For each of the four regions, run `/meta-top-digital <region>`. Confirm badge renders with correct region code, Resolved block carries correct currency and regulatory body, and a real six-section brief follows (or the v1.5 hard-block callout if observed_live is missing).
- Run `diff -q "C:/Users/HP/.claude/skills/meta-top-digital/references/regions/" "C:/Users/HP/projects/meta-top/skills/meta-top-digital/references/regions/"` — confirm zero diff after sync.
- Grep the live path for "Region not yet shipped" in `meta-top-digital/SKILL.md` — confirm the notice is removed.

---

### U4. U5 mirror AE.yaml sync + placeholder annotation (meta-top-digital only, AE)

**Goal.** Sync the AE.yaml from working copy to live path with explicit placeholder annotation. AE.yaml has unique regulatory (NMC + TRA) + Arabic-language constraints that warrant split-off from U3.

**Requirements.** R12, R13, R14.

**Dependencies.** U1, U3.

**Files.**
- `meta-top-digital/references/regions/ae.yaml` (live-path sync; authored in working copy)

**Approach.**
- Sync AE.yaml from working copy: `cp -f "C:/Users/HP/projects/meta-top/skills/meta-top-digital/references/regions/ae.yaml" "C:/Users/HP/.claude/skills/meta-top-digital/references/regions/ae.yaml"`. Verify with `diff -q`.
- Set `last_reviewed: 2026-10-01`.
- Annotate `digital_marketplaces` and `digital_categories` lists with explicit "TBD / placeholder pending Arabic-language marketplace research" notes on any list where the implementer lacks confidence in the curation. The implementer may ship with the working-copy list as a starting point, but the annotation makes the placeholder visible.
- Curate `prohibited_categories_digital` per R10/R11 + KTD5: UAE adds `forex-without-license`, `crypto-without-license` per NMC + TRA guidance. The implementer consults NMC + TRA's published guidance to author the additions.
- Bump the v1.9 entry in SKILL CONTRACT bullet 1 to note U5 AE.yaml ships with placeholder annotation.

**Patterns to follow.** Working-copy AE.yaml; live `meta-top-digital/references/regions/in.yaml` structure; v1.6 plan's mirror-sync discipline.

**Test scenarios.**
- `/meta-top-digital ae` invokes without the "Region not yet shipped" notice and returns a brief.
- AE.yaml `digital_marketplaces` and `digital_categories` lists carry explicit "TBD / placeholder" annotations where applicable.
- AE.yaml `prohibited_categories_digital` includes the UAE-specific additions (`forex-without-license`, `crypto-without-license`).

**Verification.**
- Run `/meta-top-digital ae`. Confirm the badge renders with `ae` region code, the Resolved block carries AED currency and NMC + TRA regulatory anchor, and a real brief follows.
- Read AE.yaml and confirm `last_reviewed: 2026-10-01` and the placeholder annotations where applicable.
- Run `diff -q` to confirm live-path parity with working copy.

## Scope Boundaries

### In scope

- Widening Step 3.5 trigger to the four-condition union (R1-R2).
- Dropping the Step 3.5 conditional gate; tier-0 cap unconditional ≤13 (R3).
- Raising per-invocation latency budget to ≤120s (R4).
- F16 baseline logging for empirical latency validation (R5).
- Porting the 🏆 verdict callout to `meta-top` with gate 3 wording adapted + KTD4 diff step + v1.9 changelog FYI blockquote (R6-R9).
- Syncing U5 mirror unit region YAMLs (US, CA, UK, AU) from working copy to live path with per-region `prohibited_categories_digital` curation (R10-R11, R13-R14).
- Syncing U5 mirror AE.yaml from working copy to live path with placeholder annotation (R12-R14).
- SKILL.md Pre-Flight update removing the "Region not yet shipped" notice (R13).
- v1.8 → v1.9 version bump for both skills (KTD8).

### Deferred for later

- **Sharpen weak signals via Playwright extraction (v1.9.1+).** Originally proposed as U3 in the v1.9 draft, but the premise depends on data availability the user has not yet measured (most Meta Ad Library ads carry ≤5 comments; without empirical validation, sharpening changes the source without changing informativeness). Work that was in the v1.9 draft U3 moves here as a v1.9.1 unit gated on F16 baseline data showing Playwright extraction has measurable benefit.
- **Confidence-formula recalibration (v1.9.1+).** Per v1.6 plan Q1 — gated on F16 baseline data showing formula compression.
- **Hard-block threshold relaxation (v1.9.1+).** Per v1.8 plan Q3 — gated on F16 baseline ≥30 invocations per skill tree showing empirical tier-0 success-rate justification.
- **Multi-region correlation sub-score (v2+).** Requires more regions + correlation infra; v1.9 lands U5 to enable this but does not implement the sub-score.
- **Buyer-intent signals tier-2.5 (v2+).** Requires Reddit / Quora scraping infra; out of scope per v1.6 plan future-work list.
- **`volume_proxy` sub-score (v2+).** Requires Gumroad API integration; out of scope per v1.6 plan.
- **Historical trend tracking across runs (v2+).** Snapshot semantics per v1.3 R14.
- **Paid search Python fallbacks (Brave / Serper / SerpAPI / Exa).** Out of scope per v1.5 plan non-goal.

### Outside this product's identity

- Removing the trust + ethics frame ("Category design, not content cloning").
- Removing the per-category observed-live hard-block (relaxing the threshold is in-scope as future work; removing the block is not).
- Removing the prohibition on cloning specific creator content from the Option B brief.
- Changing the six-section output structure (a-f).
- Changing the badge format (`📊 meta-top v{X} · region: {region} · {YYYY-MM-DD}`).
- Changing the v1 region list (extending it beyond `in`, `us`, `ca`, `uk`, `au`, `ae`).
- Multi-language output (English-only in v1).
- Meta Business Manager API integration (no auth, no business verification in v1).

## Open Questions

- **Q1 (carry-forward from v1.6 plan).** Confidence formula `(observed_live_count × 30) + (total_sources × 5) + (recency_bonus × 10)` may produce percentages that compress into one band once tier-0 success rates rise under v1.8 Playwright-primary. If empirical F16 baseline data shows compression, recalibrate. v1.9 ships the formula verbatim; calibration is deferred to v1.9.1+.
- **Q2 (carry-forward from v1.8 plan).** Resolved in v1.8: search engines block Playwright more aggressively than WebFetch; v1.8's open-ended discovery path degrades to tier-1 (WebSearch) under block; brief still ships. v1.9 inherits this behavior unchanged.
- **Q3 (carry-forward from v1.8 plan).** Hard-block threshold (0 of 3 → block) could raise to 1 of 3 (brief always ships with caveats) given the higher tier-0 observed_live success rate. v1.9 ships the threshold unchanged; relaxation is deferred to v1.9.1+.
- **Q5 (carry-forward from v1.8 plan).** Latency budget raise from ≤90s to ≤120s (now in v1.9 per R4 / KTD3) needs empirical validation. F16 baseline log per-invocation latency. If post-cutover median exceeds 75s, tighten to ≤11 navs in v1.9.1.
- **Q4 (new this plan).** Does the per-region `prohibited_categories_digital` curation (R10-R14) need to be reviewed periodically by a regulatory specialist, or is the v1.9 author-time curation sufficient until v2? v1.9 ships the curation as-is; periodic review cadence is a v1.9.1 question.

## System-Wide Impact

- **End user (user invoking `/meta-top` or `/meta-top-digital`).** Sees more comprehensive briefs (Step 3.5 trigger fires on more conditions), an unconditional ≤13 cap, sharper verdict under the new `meta-top` callout (with a v1.9 changelog FYI blockquote on first invocation), and full v1-region coverage in `meta-top-digital`. AE.yaml ships with placeholder annotation — users querying `/meta-top-digital ae` see a brief whose marketplace curation is acknowledged-pending.
- **Sub-agent (`meta-top-researcher`, `meta-top-digital-researcher`).** Sees the wider Step 3.5 trigger, the unconditional ≤13 cap (gate dropped), and F16 baseline logging. The cap math is no longer conditional, which simplifies the gate's complexity.
- **Per-invocation latency.** Median may rise modestly under v1.9 because the default cap is higher; F16 baseline counters measure this empirically. The latency budget headroom (≤120s) absorbs the rise.
- **Maintenance burden.** Per-region `prohibited_categories_digital` lists need periodic curation to track regulator changes. Five new region YAMLs to keep in sync with the parent `meta-top` region set — each region's `digital_categories` and `digital_marketplaces` lists need periodic refresh at the same cadence as the parent skill's 6 region YAMLs.
- **Skill scripts.** Unchanged. `scripts/keyless_search.py` and `scripts/lib/*` are byte-for-byte shared between the two skills; the working-copy mapping is preserved (canonical scripts/ lives under `meta-top/scripts/`; `meta-top-digital/scripts/` is a copy).
- **Working-copy sync.** Per the `meta-top-skill-file-paths` memory rule, the live edits land at `C:\Users\HP\.claude\skills\` and are then copied to the working copy at `C:\Users\HP\projects\meta-top\skills\`. The mirror sync (`cp -f` + `diff -q`) is the last step in every unit's verification.

## Risks & Dependencies

- **R1. Meta Ad Library rate limits under wider trigger + unconditional ≤13 cap.** More invocations hit Playwright extra navs; Meta may serve verification walls more often. Mitigation: F16 baseline logs `rate_limit_hit` and `verification_wall_hit` separately (per R5 schema); the cap stays hard at ≤13 so the worst case is bounded.
- **R2. Latency budget raise unverified empirically.** v1.8 Q5 was deferred on measurement grounds; v1.9 ships the raise on user preference without empirical validation. **This is a runtime-budget decision, not a calibration parameter** (per KTD7) — the asymmetry is deliberate. Mitigation: F16 baseline logs per-invocation latency; if median exceeds 75s, tighten in v1.9.1.
- **R3. Five new region YAMLs + per-region prohibition curation.** Each region's `prohibited_categories_digital` requires consulting the regulator's published guidance (FTC, ASA, AANA, NMC + TRA, Ad Standards + CRTC). Mitigation: KTD5's structural-port discipline + R10-R14's explicit per-region additions; AE.yaml ships with placeholder annotation for marketplace curation.
- **R4. meta-top verdict callout may surface unexpected winners under 4-gate tie-break.** The verdict is deterministic but the inputs may interact unexpectedly with meta-top's broader category set (3 seeds per region vs digital's 5 seeds). Mitigation: U2 verification invokes `/meta-top in` and confirms the callout shape is parallel to digital's; the KTD4 diff step identifies any scope divergence in `prohibited_categories`.
- **R5. AE.yaml ships with placeholder annotation.** Arabic-language digital marketplaces may not exist as a verifiable surface; the working-copy AE.yaml may have empty or fabricated lists. Mitigation: explicit "TBD / placeholder" annotations; the verification reads AE.yaml and confirms annotations are present where applicable.
- **R6. Working-copy drift.** Per the `meta-top-skill-file-paths` memory rule, edits to the working copy are not loaded by Claude. Mitigation: every unit's verification ends with a live-path grep AND a `cp -f` mirror sync.
- **R7. Playwright MCP availability.** v1.8 Playwright-primary depends on the MCP server being configured in the host environment. Mitigation: this is unchanged from v1.8; the v1.8 fail-soft behavior (tier-1 WebSearch fallback when MCP unavailable) carries forward. U3's per-region verification runs `/meta-top-digital <region>` directly; if MCP is unavailable, the verification falls back to YAML-structure-only (`python -c "import yaml; yaml.safe_load(open('references/regions/{region}.yaml'))"` to confirm parse-ability).

## Acceptance Examples

- AE1. The Step 3.5 trigger fires on `partial_research: true` even when all 3 top categories have `observed_live` examples. Triggered by: invocation with `partial_research: true` in digest. Then: cap stays at ≤13 (unconditional per KTD2); F16 baseline line written with `partial_research=1, observed_live_lacking=0`. Outcome: Playwright extra navs run if the implementer invokes the trigger logic.
- AE2. The Step 3.5 trigger fires on `rate_limit_hit: true` even when 0 of 3 categories lack `observed_live`. Triggered by: invocation with `rate_limit_hit: true` in digest. Then: cap stays at ≤13; F16 baseline line written with `rate_limit_hit=1`. Outcome: Playwright extra navs run.
- AE3. The `/meta-top in` call produces a 🏆 verdict callout naming a category, the winning_score.total, and a confidence percentage. Triggered by: standard `/meta-top in` invocation. Then: rubric lines render under Section (b); the verdict callout renders immediately after. Outcome: the user sees a single recommended category with a confidence band.
- AE4. The verdict callout is suppressed when 0 of 3 categories carry `observed_live`. Triggered by: invocation with all top-3 categories having `pricing_tier_source: inferred_seed`. Then: the v1.5 hard-block callout (`category-pricing-research-required`) renders; no verdict callout. Outcome: brief is blocked.
- AE5. The meta-top verdict callout references `prohibited_categories` (not `prohibited_categories_digital`) in gate 3, OR carries a scope qualifier if KTD4 diff identifies divergence. Triggered by: invocation whose digest has any top category in `prohibited_categories`. Then: gate 3 disqualifies that category from the winner. Outcome: the callout picks a non-prohibited category.
- AE6. `/meta-top-digital us` invokes without the "Region not yet shipped" notice and returns a real six-section brief. Triggered by: standard invocation. Then: the Resolved block carries `Region: United States (us)` with USD currency and FTC regulatory anchor. Outcome: a brief follows (or the v1.5 hard-block callout if observed_live is missing).

## Sources & Research

- **v1.3 winning-product framework plan**: `docs/plans/2026-09-27-winning-product-framework-plan.md`. Canonical source for the 6-signal rubric, 14-max ceiling, band thresholds, underground-signals callout, and post-menu option 5.
- **v1.4 Meta Ad Library tier-0 plan**: `docs/plans/2026-09-28-meta-ads-library-tier0-v14.md`. Genesis of tier-0 Playwright as the authoritative source for longevity / variants / cross_country.
- **v1.5 anti-fabrication hard-block plan**: `docs/plans/2026-09-29-meta-top-digital-v15-improvements.md`. 4-value `pricing_tier_source` enum, per-category hard-block, 5-column pricing table.
- **v1.6 winning-verdict plan**: `docs/plans/2026-09-29-1530-feat-meta-top-digital-v16-winning-verdict-plan.md`. 4-gate tie-break (KTD1), R4 confidence formula, R3 skip rule, R6 band thresholds. Decision-by-omission (KTD4) for meta-top asymmetry — closed by U2 of this plan.
- **v1.7 realtime tier-4 fix plan**: `docs/plans/2026-09-29-feat-meta-top-digital-v17-realtime-tier4-fix-plan.md`. Rate-limit + 403/404 recovery; cache scope (search-results only); appendix explicit handoff to memory rule (R1 widening).
- **v1.8 Playwright-primary plan**: `docs/plans/2026-09-29-feat-meta-top-digital-v18-playwright-primary-plan.md`. Tier-0 absorption of tier-3 and tier-4; cap rebalance ≤9 → ≤13; cap-raise gate step (Step 3.5). Open questions Q3, Q5 — addressed by this plan.
- **`meta-top-digital-full-research-default` memory**: `meta-top-digital-full-research-default.md`. Trigger condition the spec has held since 2026-09-28 — U1 closes the spec/memory drift.
- **`meta-top-skill-file-paths` memory**: `meta-top-skill-file-paths.md`. Working-copy vs live-path distinction; every unit's verification ends with a live-path grep + mirror sync.
- **Live SKILL.md and researcher specs**: `meta-top/SKILL.md`, `meta-top/references/agents/meta-top-researcher.md`, `meta-top-digital/SKILL.md`, `meta-top-digital/references/agents/meta-top-digital-researcher.md`.
- **Live region YAMLs**: `meta-top/references/regions/{in,us,ca,uk,au,ae}.yaml` (parent skill's 6 regions are the reference template); `meta-top-digital/references/regions/in.yaml` (the v1 shipping contract for shape — KTD5).
- **Working-copy region YAMLs**: `C:\Users\HP\projects\meta-top\skills\meta-top-digital\references\regions\{us,ca,uk,au,ae}.yaml` — already authored; U3 + U4's work is verification + sync, not authoring.