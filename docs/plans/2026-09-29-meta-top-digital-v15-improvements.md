---
plan_id: 2026-09-29-meta-top-digital-v15
created: 2026-09-29
supersedes: 2026-09-28-meta-ads-library-tier0-v14 — additive, not replacing
target_skills:
  - meta-top
  - meta-top-digital
target_version: v1.5
status: draft, awaiting user approval
---

# v1.5 — meta-top-digital: in-depth research + real live data integrity

## Goal

Move meta-top-digital and meta-top from "snapshot with inferred ranges" to "in-depth, real-live, audit-trailed" — every cited price is either truly observed (with `accessed_at` + tier + source URL), inferred (clearly labeled), or absent (no fabrication). Tier-0 Meta Ads Library becomes per-category with cross-region sweep. Output renders audit metadata inline next to every citation.

## Why now

User feedback 2026-09-29 (verbatim): *"how can I make this slash command better? I want the research to be in depth and the result should be based on real live data and not fabrication."*

Concrete failures from the v1.4 IN run on 2026-09-29:

| # | Failure mode | Severity | Source line |
|---|---|---|---|
| F1 | "Range inferred from India-region search snippet; specific listing price not in snippet" labeled as `pricing_tier_source: observed` | High (hard-block integrity) | notion-templates, spreadsheet, design-assets, ebook-bundles pricing_examples |
| F2 | Tier-0 used 1 nav for 5 categories -> variants sub-score 0/3 across the board | High (winning-product framework blind) | researcher.md Step 3.0 single-keyword nav |
| F3 | Cross-country sub-score proxied via "EU transparency flag" -> not a real cross-region observation | Medium (sub-score integrity) | researcher.md cross_country |
| F4 | Benchmarks returned "Insufficient public data" -> brief shipped without CPM/CPC/CPV/CTR for India | Medium (decision-usability) | benchmarks block |
| F5 | Tier-4 skipped because tier-3 contributed >=1 observed source -> lost the chance to verify other categories via Playwright | Medium (depth) | tier-4 trigger logic |
| F6 | Secondary blog roundups (kupkaike, ownstreet, paisadollar, getvik, aiunpacker) outweighed primary sources (Meta Library, Gumroad product pages) | Medium (source quality) | evidence_urls mix across categories |
| F7 | Brief shipped despite 4 of 5 categories having zero truly-observed pricing examples | High (hard-block over-relaxed) | SKILL.md hard-block wording |
| F8 | Citations in chat brief carry no `accessed_at` or tier label -> user can't tell which came from where | Low (audit) | output rendering |
| F9 | No baseline-scoring sandbox -> no way to detect skill regressions in future runs | Low (regression safety) | out of scope today; defer |
| F10 | No snapshot-id versioning -> price drift across runs invisible | Low (drift visibility) | out of scope today; defer |

## Non-goals (explicit)

- ❌ Drop or replace v1.4 tier-0 (Meta Ads Library stays mandatory first-tier)
- ❌ Drop the trust+ethics frame "Category design, not content cloning"
- ❌ Auto-clear `confidence: low` based on tier-0 evidence (the v1.4 caveat stands)
- ❌ Increase total Playwright navigation budget beyond <=7 per invocation (5 tier-0 + 2 tier-4)
- ❌ Add paid-search Python fallbacks (Brave / Serper / SerpAPI / Exa) — v1.5+
- ❌ Touch `references/regions/*.yaml` files except to add benchmark proxy anchors

## Design decisions

1. **Two-tier pricing-source label** — `pricing_tier_source` becomes an enum: `observed_live | observed_snippet | inferred_seed | unverified`. Only `observed_live` clears the hard-block. `observed_snippet` carries a `snippet_text` field showing the actual extracted text. `inferred_seed` is the seed-anchor default; `unverified` is "no source could be obtained".
2. **Per-category hard-block** — brief ships only when **all 3 top categories** have >=1 `observed_live` pricing example. If any of the top 3 lacks `observed_live`, that category surfaces the `category-pricing-research-required` blockquote in section (b), and Option B's pricing tier table marks its tiers `[unverified starting points, not observed-live]` inline.
3. **Tier-0 per-category nav** — one keyword query per top category. For 5 top categories, that's 5 tier-0 navigations.
4. **Cross-region sweep** — for each top category, tier-0 navigates `country=IN` first; if IN returned <30 ads, sweep `country=US` and `country=UK` to populate cross_country. Cap at <=3 cross-region navigations per category, fold into the per-category tier-0 budget.
5. **Source-tier cap** — secondary blog roundups capped at 30% of citations per category; primary sources >=70%. The digest's `data_quality_note` surfaces the actual ratio.
6. **Tier-4 trigger** — fire Playwright on any tier-3 403 OR >=2 inferred pricing examples in a category, regardless of observed count.
7. **Benchmarks tier-3.5** — new rung between tier-3 and tier-4. Uses Meta Ad Library's advertiser-name search to count active ads per category in IN; pair with industry-known CPM proxy ranges from the v1.3 skill's benchmarks lookup when >=2 advertiser-count observations clear. Renders as CPM range `[low, high]` in INR/1k impressions.
8. **Audit metadata inline** — every citation `[name](url)` in the chat brief is followed by `accessed YYYY-MM-DD tier N kind X` as inline suffix. The digest's per-citation audit metadata flows through to the rendered output.
9. **Snapshot versioning** — every brief carries `--snapshot-id <YYYY-MM-DD-HHMM-region>` in the badge. The brief footer surfaces `price_drift_since_last_run` for each category when a prior snapshot exists.

### Budget Reconciliation

| Tier | v1.4 cap | v1.5 cap | Why |
|---|---|---|---|
| Tier-0 (Meta Ads Library) | <=1 nav | <=5 navs (1 per top category) | per-category keyword nav for variants/cross_country |
| Cross-region sweep | n/a | <=3 navs per category, fold into tier-0 budget | stay within effective cap |
| Tier-4 (Playwright fallback) | <=2 navs | <=2 navs (unchanged) | trigger relaxed; cap unchanged |
| **Total Playwright** | <=3 | <=7 (5 tier-0 + 2 tier-4) | total cap raised from 3 to 7; record in badge footer |
| WebFetch calls | <=20 | <=20 (unchanged) | ladder ceiling stays |

If the user's host reports latency budget concerns, U3 (cross-region) folds back into a single `country=IN` query and the effective cap drops back to <=5.

## Unit list

### U1 — Anti-fabrication: stricter source labeling + per-category hard-block
**Files:**
- Live path (meta-top-digital): `C:\Users\HP\.claude\skills\meta-top-digital\SKILL.md`
- Live path (meta-top): `C:\Users\HP\.claude\skills\meta-top\SKILL.md` (mirror)
- Live path (meta-top-digital researcher): `C:\Users\HP\.claude\skills\meta-top-digital\references\agents\meta-top-digital-researcher.md`
- Live path (meta-top researcher): `C:\Users\HP\.claude\skills\meta-top\references\agents\meta-top-researcher.md` (mirror)
- Working-copy paths: mirror in `C:\Users\HP\projects\meta-top\skills\meta-top{,-digital}/...`

**Edit 1a (SKILL.md, both skills):** Replace `pricing_tier_source: observed` with the four-value enum: `observed_live | observed_snippet | inferred_seed | unverified`. Add inline definitions after the badge contract.

**Edit 1b (SKILL.md, both skills):** Rewrite the Hard-Block section:
- Current: brief ships if **any** category has `observed` pricing
- New: brief ships if **all 3 top categories** have `pricing_tier_source: observed_live` for >=1 pricing tier
- If a top-3 category lacks `observed_live`, that category surfaces the blockquote in its section (b), and Option B's pricing tier table marks its tiers `[unverified starting points, not observed-live]` inline
- Brief still ships (just with caveats) — only full block if 3 of 3 top categories lack `observed_live`

**Edit 1c (researcher.md, both skills):** Update the JSON digest schema's `pricing_examples[].pricing_tier_source` to be the four-value enum, plus new optional field `snippet_text: string` (the actual text extracted) when `observed_snippet`.

**Verification:**
```bash
grep -c "observed_live" "C:/Users/HP/.claude/skills/meta-top-digital/SKILL.md"
grep -c "observed_snippet" "C:/Users/HP/.claude/skills/meta-top-digital/SKILL.md"
grep -c "all 3 top categories" "C:/Users/HP/.claude/skills/meta-top-digital/SKILL.md"
```

### U2 — Tier-0 per-category navigation
**Files:**
- Live path (researcher.md, both skills)
- Working-copy paths: mirror

**Edit:** Replace the v1.4 tier-0 paragraph with:
```
### Tier 0 — Meta Ads Library via Playwright (per-category, v1.5+)

For EACH top-3 category (top categories from the YAML's `digital_categories` plus any live-replacement categories with >=2 cited sources), fire one `browser_navigate` to `https://www.facebook.com/ads/library/?active_status=active&country={region_code}&q={category-keyword}` where `{category-keyword}` is the category's slug-style keyword (e.g., `notion-template`, `chatgpt-prompt`, `excel-budget`). Use `browser_snapshot` (a11y-tree) to extract per-category ad IDs, advertiser names, and first-seen dates. Compute:
- **longevity** — per-category: days since ad first appeared; 30+ -> 2/3; 90+ -> 3/3
- **variants** — per-category: count sibling ads per advertiser; 5-10 -> 2/3; 20+ -> 3/3
- **cross_country** — see U3 (cross-region sweep)
```

**Edit 2b (SKILL.md, both skills):** Add budget callout: "Tier-0 cap raised from <=1 to <=5 in v1.5 (per-category keyword nav); total Playwright nav budget <=7 (5 tier-0 + 2 tier-4)."

**Verification:**
```bash
grep -c "per-category" "C:/Users/HP/.claude/skills/meta-top-digital/references/agents/meta-top-digital-researcher.md"
grep -c "<=5" "C:/Users/HP/.claude/skills/meta-top-digital/SKILL.md"
```

### U3 — Cross-region sweep
**Files:**
- Live path (researcher.md, both skills) + meta-top-digital SKILL.md mirror

**Edit 3a (researcher.md):** Append to tier-0:
```
**Cross-region sweep (v1.5+):** For each top-3 category, after the `country=IN` query, sweep `country=US` and `country=UK` (<=3 cross-region navs per category, fold into per-category tier-0 budget). Compute cross_country sub-score from observed overlap:
- Same advertiser + same ad creative across 2-3 countries -> 1/2
- Same advertiser + same ad creative across 5+ countries -> 2/2
- No observed overlap -> 0/2 (downgrade from v1.4's "EU transparency flag" proxy)

For non-IN regions, sweep IN + UK + US as the cross-region set.
```

**Edit 3b (SKILL.md):** Replace v1.4's `cross_country` sub-score definition with the v1.5 observed-overlap definition.

**Verification:**
```bash
grep -c "observed overlap" "C:/Users/HP/.claude/skills/meta-top-digital/references/agents/meta-top-digital-researcher.md"
```

### U4 — Source-tier diversification cap (30% secondary)
**Files:**
- Live path (researcher.md, both skills)

**Edit:** Add to Step 2 (digest rendering rules):
```
**Source-tier diversification (v1.5+):** Citations per category must comprise >=70% primary sources (Meta Ad Library, Gumroad product pages, Instamojo top-sellers, Canva Creators, Lemon Squeezy, Notion Marketplace) and <=30% secondary sources (blog roundups, case studies, third-party guides). If a category exceeds 30% secondary, surface in `data_quality_note: "Category X has N% secondary sources — primary-source augmentation recommended"`. Mark secondary citations with `(secondary)` inline suffix in the chat brief.
```

**Verification:**
```bash
grep -c "(secondary)" "C:/Users/HP/.claude/skills/meta-top-digital/SKILL.md"
grep -c "70%" "C:/Users/HP/.claude/skills/meta-top-digital/SKILL.md"
```

### U5 — Benchmarks tier-3.5 (Meta Library advertiser-count proxy)
**Files:**
- Live path (SKILL.md, both skills) + researcher.md mirror

**Edit 5a (SKILL.md):** Insert a new tier 3.5 in the ladder section:
```
3.5. **Benchmarks tier-3.5 (v1.5+, 2026-09-29)** — when tier 3 returns <2 CPM/CPC/CPV/CTR observed sources AND tier-0 already contributed >=1 advertiser name from Meta Library, run `WebFetch` on `https://www.facebook.com/ads/library/?active_status=active&country={region_code}&q={category-keyword}` and count distinct advertiser names in the result page. Pair with industry-known CPM proxy ranges from the v1.3 skill's benchmarks lookup (`references/benchmarks/{region}.yaml`) when >=2 advertiser-count observations clear. Renders as CPM range `[low, high]` in INR/1k impressions for IN, $/1k for US, etc. **Skip if Playwright tier-0 didn't surface >=1 advertiser name** — fall through to "Insufficient public data" + Meta Library handoff.
```

**Edit 5b (researcher.md):** Add tier-3.5 paragraph mirror.

**Verification:**
```bash
grep -c "tier 3.5\|tier-3.5\|3\.5\." "C:/Users/HP/.claude/skills/meta-top-digital/SKILL.md"
```

### U6 — Output structure polish (Option B inline column, dashboard row-level confidence)
**Files:**
- Live path (SKILL.md, both skills)

**Edit 6a (Option B rendering):** Add a `pricing_tier_source` column to the pricing tiers table:
```
| Tier | Price | Source | `pricing_tier_source` |
|---|---|---|---|
| Entry | INR 199 | seed anchor | `inferred_seed` |
| Mid | INR 599 | NKBJDigital | `observed_live` |
| Premium | INR 1999 | seed anchor | `inferred_seed` |
```

**Edit 6b (dashboard rendering):** Add a `Confidence` column to the winning-product dashboard:
```
| Score | Band | Category | Top signal | Sources | Confidence |
|---|---|---|---|---|---|
| 7/14 | promising | prompt-packs | engagement 2/3 | 5 | medium (tier-0 partial) |
```

Confidence levels: `high` (>=3 sub-scores with `confidence: high`), `medium` (>=2 with `confidence: medium`+), `low` (otherwise).

**Verification:**
```bash
grep -c "pricing_tier_source.*column\|observed_live" "C:/Users/HP/.claude/skills/meta-top-digital/SKILL.md"
grep -c "| Confidence |" "C:/Users/HP/.claude/skills/meta-top-digital/SKILL.md"
```

### U7 — Tier-4 trigger relaxation
**Files:**
- Live path (meta-top-digital SKILL.md only) — meta-top has no tier-4

**Edit:** Replace the tier-4 trigger:
- Current: "when tier 3 returns 403/404 on >=2 marketplace URLs OR pricing_examples is empty"
- New: "fire when tier 3 returns 403/404 on >=1 marketplace URL OR >=2 inferred pricing examples in a category"

**Verification:**
```bash
grep -c ">=2 inferred pricing examples" "C:/Users/HP/.claude/skills/meta-top-digital/SKILL.md"
```

### U8 — Per-citation audit metadata inline
**Files:**
- Live path (researcher.md, both skills)

**Edit 8a (researcher.md rendering):** Add rendering rule:
```
**Audit metadata (v1.5+):** Every `[name](url)` citation in the chat brief MUST be followed by the inline suffix `accessed YYYY-MM-DD tier N kind X`. Example:
`[NKBJDigital — ChatGPT Prompt Pack](https://nkbjdigital.com/Product/chatgpt-prompt-pack) accessed 2026-09-29 tier 3 kind marketplace`

The audit suffix is added by the orchestrator at render time from the digest's per-source `accessed_at` + `tier_used` (new field) + `kind` fields.
```

**Edit 8b (researcher.md JSON schema):** Add `tier_used: 0|1|2|3|3.5|4|5` to each source object in the digest.

**Verification:**
```bash
grep -c "accessed YYYY-MM-DD" "C:/Users/HP/.claude/skills/meta-top-digital/SKILL.md"
grep -c "tier_used" "C:/Users/HP/.claude/skills/meta-top-digital/references/agents/meta-top-digital-researcher.md"
```

### U9 — Snapshot versioning + price-delta reporting (footer)
**Files:**
- Live path (SKILL.md, both skills) + 2x researcher.md

**Edit 9a (badge contract):** Add to badge format:
```
Badge format: `meta-top-digital v1.5 region: {region} {YYYY-MM-DD-HHMM} snapshot {snapshot_id}`. The snapshot_id is `{region}-{YYYY-MM-DD-HHMM}-{8-char-hash-of-yaml-path}`.
```

**Edit 9b (footer):** Add `price_drift_since_last_run` block:
```
**Price drift (v1.5+):** When a prior snapshot for this region exists, surface a `price_drift_since_last_run` table showing per-category observed-live price changes between snapshots. Drift >20% flagged for review.
```

**Edit 9c (researcher.md):** Add `snapshot_id` field to the JSON digest root.

**Verification:**
```bash
grep -c "snapshot_id" "C:/Users/HP/.claude/skills/meta-top-digital/SKILL.md"
grep -c "price_drift_since_last_run" "C:/Users/HP/.claude/skills/meta-top-digital/SKILL.md"
```

### U10 — Working-copy mirror + sync check
**Files:** No new files; runs sync from live to working copy for all touched files (SKILL.md and researcher.md for both skills = 4 files total).

**Edit:** After U1-U9 land on the live paths, sync each live file to its working-copy twin via `cp -f`. Run `diff -q` to confirm 0 diff lines on all 4 pairs.

**Verification:**
```bash
diff -q "C:/Users/HP/.claude/skills/meta-top-digital/SKILL.md" "C:/Users/HP/projects/meta-top/skills/meta-top-digital/SKILL.md"
diff -q "C:/Users/HP/.claude/skills/meta-top-digital/references/agents/meta-top-digital-researcher.md" "C:/Users/HP/projects/meta-top/skills/meta-top-digital/references/agents/meta-top-digital-researcher.md"
diff -q "C:/Users/HP/.claude/skills/meta-top/SKILL.md" "C:/Users/HP/projects/meta-top/skills/meta-top/SKILL.md"
diff -q "C:/Users/HP/.claude/skills/meta-top/references/agents/meta-top-researcher.md" "C:/Users/HP/projects/meta-top/skills/meta-top/references/agents/meta-top-researcher.md"
```

## Out of scope (deferred to v1.6+)

- ❌ Per-region baseline scoring sandbox (F9) — needs YAML infrastructure + regression detector
- ❌ Adversarial test cases (known-bad categories that should fail hard-block)
- ❌ Multi-language output (still English-only)
- ❌ `--last=N` time-window flag (still snapshot semantics)
- ❌ A/B testing of Meta ad creative (still out — Meta platform feature)

## Hard-blocks (within this plan)

- ❌ NO change to trust+ethics frame ("Category design, not content cloning")
- ❌ NO change to v1.4 tier-0 mandatory status
- ❌ NO silent upgrade of any `observed` label to `observed_live`
- ❌ NO increase beyond <=7 Playwright navigations per invocation
- ❌ NO removal of secondary blog sources entirely (capped, not banned)

## User-level constraints (carry forward)

- ✅ **No Claude Code footer** in any commit messages or PR/PR-description bodies (user-level rule, all repos)
- ✅ **Scope discipline** — commit/push ONLY files in each unit's Files: list
- ✅ **Skill file paths** — edit live path under `C:\Users\HP\.claude\skills\`, not working-copy
- ✅ Use **absolute paths**; verify with grep on the live path, not the working-copy
- ✅ Per-category winning-product rubric format preserved (v1.3 14-max ceiling)

## Files index

| Unit | Live path (Claude Code loads this) | Working-copy mirror |
|---|---|---|
| U1 | meta-top-digital/SKILL.md + meta-top/SKILL.md + 2x researcher.md | skills/meta-top{,-digital}/... |
| U2 | 2x researcher.md + 2x SKILL.md | mirror |
| U3 | 2x researcher.md + meta-top-digital/SKILL.md | mirror |
| U4 | 2x researcher.md | mirror |
| U5 | 2x SKILL.md + 2x researcher.md | mirror |
| U6 | 2x SKILL.md | mirror |
| U7 | meta-top-digital/SKILL.md only (meta-top has no tier-4) | mirror |
| U8 | 2x researcher.md | mirror |
| U9 | 2x SKILL.md + 2x researcher.md | mirror |
| U10 | (sync-only) | n/a |

## Post-approval next step

Run `/ce-work` with this plan file. `ce-work` should:
1. Execute U1 -> U9 in order — each is one or more Edit calls against the live paths
2. Run U10 sync after U1-U9 land
3. Run `ce-code-review` against the changed files
4. Stop and surface results for ship/no-ship decision (no auto-commit per the no-claude-footer rule + scope-discipline rule)

If `ce-work` is unavailable, the same flow runs inline as ~15 Edit calls + 1 sync round, all against live paths.

## Rollback plan (if v1.5 ships and regresses)

- Revert commit via `git revert <v1.5-commit-sha>` — all v1.4 paths preserved by additive design
- Re-run `/meta-top-digital in` to verify v1.4 baseline restored
- File the regression in `docs/post-mortems/YYYY-MM-DD-v15-regression.md` with the failing category + observed behavior
