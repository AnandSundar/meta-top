---
plan_id: 2026-09-28-meta-ads-library-tier0
created: 2026-09-28
supersedes: 2026-09-27-winning-product-framework-plan (v1.3) — additive, not replacing
target_skills:
  - meta-top
  - meta-top-digital
target_version: v1.4
status: draft, awaiting user approval
---

# v1.4 — Meta Ads Library as Tier-0 (mandatory source + Playwright access)

## Goal

Make Meta Ads Library the **first-priority source** for the three ad-inventory signals of the v1.3 winning-product rubric (longevity / variants / cross_country), accessed via Playwright, in BOTH `meta-top` and `meta-top-digital` skills. Tier-0 is additive — the existing 5-tier ladder (WebSearch → DDG → curated marketplaces → Playwright fallback → curated anchors) stays intact.

## Why now

User feedback 2026-09-28 (verbatim): *"I want you to prioritize meta ads library for finding winning products so I can copy them. use playwright to do this. Add this as a mandatory step to the skill as well."*

- Meta Ad Library is the **only first-party source** for ad-level longevity (Meta doesn't kill unprofitable ads → time-in-market is the strongest winning signal at the framework level)
- Variants count per advertiser is most directly observed on Meta Ad Library (click advertiser → see all current ads → count)
- Cross-country rollout is observable via `country=IN|US|CA|UK|AU|AE` filter params
- WebSearch returns zero ad-level evidence; tier-3 curated marketplaces cannot show ad inventory; WebFetch 403s on Facebook's anti-bot layer
- Playwright bypasses 403s (as proven by Etsy tier-4 escalation earlier this session)

## Non-goals (explicit)

- ❌ Drop or replace any of the existing 5 tiers — tier-0 is **additive above tier-1**, the rest stay
- ❌ Drop the trust+ethics frame **"Category design, not content cloning"** — keep intact (user confirmed 2026-09-28: *"Keep the frame intact (Recommended)"*)
- ❌ Allow literal cloning of specific creator ad copy into the user's brief
- ❌ Increase total Playwright navigation budget beyond the **new split: ≤1 tier-0 + ≤2 tier-4 = ≤3 per invocation** (existing cap was ≤2 tier-4 only)
- ❌ Add tier-0 evidence for the OTHER 3 signals (engagement / marketplace / pain_signal) — those still use existing ladder sources
- ❌ Touch `references/regions/*.yaml` files or `digital_marketplaces` anchors

## Design decisions

1. **Tier-0 = Meta Ads Library only.** URL pattern: `https://www.facebook.com/ads/library/?active_status=active&country=<REGION>` where `<REGION>` comes from the YAML's `region_code`.
2. **Cap: ≤1 Playwright navigation per invocation, separate budget from tier-4's ≤2.** Total ≤3 Playwright navigations per invocation across both tiers.
3. **Mandatory status:** tier-0 fires whenever the research prompt requires longevity / variants / cross_country scoring. Falls through to tier-1 if tier-0 hits Meta's verification wall (login/CAPTCHA) or Playwright is unavailable.
4. **Sub-score routing:** the three ad-inventory signals (`longevity`, `variants`, `cross_country`) score from tier-0 evidence first; tier-1 through tier-3 become **confirmation/qualification** sources, not authoritative for these signals.
5. **Confidence boost:** when tier-0 contributes evidence for at least one of the three signal sub-scores, the **category-level `confidence: low` flag downgrades to `confidence: medium`** for those sub-scores (the `confidence: low` rule on the parent winning-score stays — see Sub-Score Caveats below).
6. **Trust+ethics:** tier-0 surfaces **patterns** (longevity / variants / cross-country), not specific creator ad copy to clone. The "Category design, not content cloning" line stays verbatim in Option B.
7. **Mirror across both skills:** `meta-top` and `meta-top-digital` get identical tier-0 structure. Per user approval 2026-09-28: *"Both skills, via plan file (Recommended)"*.

### Sub-Score Caveats (gating tier-0 applicability)

The `confidence: low` parent rule fires when the live research returned **fewer than 5 sources** for the region — that rule stays in v1.4. Tier-0 contributing at least one sub-score evidence entry satisfies one source, but does NOT auto-clear `confidence: low` at the category level (this avoids gaming a low-evidence region by leaning on Meta's free inventory). Concrete:

| Tier-0 contribution | Sub-score confidence | Category confidence |
|---|---|---|
| 0 of 3 (tier-0 failed completely) | unchanged (low) | unchanged (low) |
| 1–3 of 3 (tier-0 contributed) | downgrades low → medium for those sub-scores | stays low unless region's other-tier sources ≥ 5 |

## Unit list

### U1 — `references/agents/meta-top-digital-researcher.md` Step 3.0: insert tier-0
**Files:**
- **Live path (MUST land here for skill to pick up):** `C:\Users\HP\.claude\skills\meta-top-digital\references\agents\meta-top-digital-researcher.md`
- **Working-copy path (mirror only, sync at end):** `C:\Users\HP\projects\meta-top\skills\meta-top\references\agents\meta-top-digital-researcher.md`

**Edit:** In Step 3.0 (source ladder), insert the following tier-0 paragraph as the FIRST tier, before tier 1 (WebSearch):

````markdown
### Tier 0 — Meta Ads Library via Playwright (mandatory, v1.4+)

Always fire `browser_navigate` to `https://www.facebook.com/ads/library/?active_status=active&country={region_code}` **before** tier 1 when the orchestrator needs longevity / variants / cross_country signal. Capture ad IDs + advertiser names + first-seen dates via `browser_snapshot` (a11y-tree), then construct the three sub-scores:

- **longevity** — filter by `active_status=active`, count days since ad first appeared in Library (30+ → 2/3; 90+ → 3/3).
- **variants** — click advertiser, count sibling ads in same Library entry (5–10 → 2/3; 20+ → 3/3; <3 → 0/3; 3–4 → 1/3 interpolating).
- **cross_country** — same ad across multiple `country=` filter values (2–3 → 1/2; 5+ → 2/2).

**Mandatory for these 3 sub-scores** — tier-1 through tier-3 are no longer authoritative for them, only confirmation/qualification. **Cap: ≤1 Playwright navigation per invocation**, separate from tier-4's ≤2 budget. **Browser automation only** (no `pip install playwright`) — requires the `playwright` MCP server configured in the host environment. Fall through to tier 1 if tier-0 hits Meta's verification wall (login/CAPTCHA) or Playwright is unavailable.

Trust + ethics: tier-0 surfaces **patterns** (longevity, variants, cross-country) — NOT specific creator ad copy to clone. The "Category design, not content cloning" line stays intact.
````

**Version bump:** change any "v1.3" reference in this file to "v1.4".

**Verification:**
```bash
grep -c "Tier 0 — Meta Ads Library" "C:/Users/HP/.claude/skills/meta-top-digital/references/agents/meta-top-digital-researcher.md"   # expect 1
grep -c "≤1 Playwright navigation" "C:/Users/HP/.claude/skills/meta-top-digital/references/agents/meta-top-digital-researcher.md"   # expect ≥1
```

### U2 — `SKILL.md` (meta-top-digital): source-ladder section + badge
**Files:**
- **Live path:** `C:\Users\HP\.claude\skills\meta-top-digital\SKILL.md`
- **Working-copy path (mirror):** `C:\Users\HP\projects\meta-top\skills\meta-top\SKILL.md`

**Edit:**
1. Update header/banner from `v1.3` to `v1.4` and add a one-line v1.4 change note: *"v1.4 (2026-09-28): tier-0 = Meta Ads Library via Playwright, mandatory for longevity/variants/cross_country."*
2. In "Reliability: source ladder (v1.2+, mirror of meta-top v1.1)" section, insert tier-0 above tier 1:

````markdown
0. **Meta Ads Library via Playwright (v1.4+, mandatory)** — `browser_navigate` to `https://www.facebook.com/ads/library/?active_status=active&country={region}` and extract ad-inventory signals (longevity / variants / cross_country) via `browser_snapshot`. **Cap: ≤1 Playwright navigation per invocation** (separate budget from tier-4). **Mandatory** when any of the three ad-inventory sub-scores is required. Falls through to tier 1 if Playwright is unavailable or Meta serves a verification wall.
````

3. Update the existing source-ladder intro sentence to acknowledge tier-0 fires first.
4. Update the Hard-Block section to add: *"Tier-0 (Meta Ads Library) is the authoritative source for longevity / variants / cross_country sub-scores in v1.4+. The Hard-Block on observed pricing tiers is independent of tier-0 and remains unchanged."*

**Verification:**
```bash
grep -c "v1.4" "C:/Users/HP/.claude/skills/meta-top-digital/SKILL.md"   # expect ≥1
grep -c "Meta Ads Library" "C:/Users/HP/.claude/skills/meta-top-digital/SKILL.md"   # expect ≥1
```

### U3 — `references/agents/meta-top-researcher.md` (mirror of U1)
**Files:**
- **Live path:** `C:\Users\HP\.claude\skills\meta-top\references\agents\meta-top-researcher.md`
- **Working-copy path (mirror):** `C:\Users\HP\projects\meta-top\skills\meta-top\references\agents\meta-top-researcher.md`

**Edit:** Mirror U1's tier-0 insertion verbatim. Same `https://www.facebook.com/ads/library/?active_status=active&country={region_code}` pattern. Same `<=1 nav, mandatory for the 3 ad-inventory signals, trust+ethics frame preserved` rules. Physical-product context: the same pattern surfaces physical-D2C winning ads (longevity = replica of winner longevity calc; variants = count of sibling ads from one advertiser; cross-country = same ad rolling across regions).

**Version bump:** change v1.3 → v1.4 in this file.

**Verification:**
```bash
grep -c "Tier 0 — Meta Ads Library" "C:/Users/HP/.claude/skills/meta-top/references/agents/meta-top-researcher.md"   # expect 1
```

### U4 — `SKILL.md` (meta-top) (mirror of U2)
**Files:**
- **Live path:** `C:\Users\HP\.claude\skills\meta-top\SKILL.md`
- **Working-copy path (mirror):** `C:\Users\HP\projects\meta-top\skills\meta-top\SKILL.md`

**Edit:** Mirror U2 verbatim. Update badge to v1.4, add v1.4 change note, insert tier-0 above tier 1 in source-ladder section, update Hard-Block section.

**Verification:**
```bash
grep -c "v1.4" "C:/Users/HP/.claude/skills/meta-top/SKILL.md"   # expect ≥1
grep -c "Meta Ads Library" "C:/Users/HP/.claude/skills/meta-top/SKILL.md"   # expect ≥1
```

### U5 — Working-copy mirror + sync check (Belt-and-suspenders for the live-paths-not-loaded memory rule)
**Files:** No new files; runs sync from live → working copy for **all 4 files** to keep the working-copy draft buffer in step with the live paths after the edits.

**Edit:** After U1–U4 land on the live paths, sync each live file to its working-copy twin via copy. The `meta-top-skill-file-paths` memory rule says Claude Code loads from `~/.claude/skills/`, not the working copy — but keeping the working copy in sync protects against future drift if someone edits the wrong path.

**Verification:**
```bash
# Confirm live and working-copy match for all 4 files
diff -q "C:/Users/HP/.claude/skills/meta-top-digital/SKILL.md"              "C:/Users/HP/projects/meta-top/skills/meta-top/SKILL.md"
diff -q "C:/Users/HP/.claude/skills/meta-top-digital/references/agents/meta-top-digital-researcher.md" "C:/Users/HP/projects/meta-top/skills/meta-top/references/agents/meta-top-digital-researcher.md"
diff -q "C:/Users/HP/.claude/skills/meta-top/SKILL.md"                       "C:/Users/HP/projects/meta-top/skills/meta-top/SKILL.md"
diff -q "C:/Users/HP/.claude/skills/meta-top/references/agents/meta-top-researcher.md"              "C:/Users/HP/projects/meta-top/skills/meta-top/references/agents/meta-top-researcher.md"
# Expect 0 diff lines on all four.
```

## Out of scope (deferred)

- ❌ Update `references/regions/*.yaml` files (region anchor lists unchanged)
- ❌ Add a new entry to `digital_marketplaces` (Meta Ads Library is a tier-0 source, not a tier-3 marketplace)
- ❌ Modify the post-menu / option flow in either SKILL.md
- ❌ Add a `creative_similarity_threshold` check (would require loosening the trust+ethics frame, which user declined)
- ❌ Integration smoke (separate unit — not auto-included per the previous plan's U17 precedent of doing smoke as a unit, but that was the FIRST plan; for this additive plan the user wants the spec ships without invoking Meta from inside this execution)

## Hard-blocks (within this plan)

- ❌ NO change to the trust+ethics frame ("Category design, not content cloning")
- ❌ NO change to the existing 5-tier ladder structure (tier-0 is additive above)
- ❌ NO increase to total Playwright navigation budget (cap stays at ≤1 tier-0 + ≤2 tier-4 = ≤3)
- ❌ NO literal-cloning language added to the brief
- ❌ NO change to `references/regions/*.yaml` or `digital_marketplaces`

## User-level constraints (carry forward from `2026-09-27-winning-product-framework-plan`)

- ✅ **No Claude Code footer** in any commits or PR/PR-description bodies (user-level rule, all repos)
- ✅ **Scope discipline** — commit/push ONLY files in each unit's Files: list; prose mentions of paths are not authorization
- ✅ **Skill file paths** — edit the live path under `C:\Users\HP\.claude\skills\`, not the working-copy path under `C:\Users\HP\projects\meta-top\skills\` (per `meta-top-skill-file-paths` memory)
- ✅ Use **absolute paths** under `C:\Users\HP\.claude\skills\`; verify with grep on the live path, not the working-copy path

## Files index

| Unit | Live path (Claude Code loads this) | Working-copy path (mirror) |
|---|---|---|
| U1 | `C:\Users\HP\.claude\skills\meta-top-digital\references\agents\meta-top-digital-researcher.md` | `C:\Users\HP\projects\meta-top\skills\meta-top\references\agents\meta-top-digital-researcher.md` |
| U2 | `C:\Users\HP\.claude\skills\meta-top-digital\SKILL.md` | `C:\Users\HP\projects\meta-top\skills\meta-top\SKILL.md` |
| U3 | `C:\Users\HP\.claude\skills\meta-top\references\agents\meta-top-researcher.md` | `C:\Users\HP\projects\meta-top\skills\meta-top\references\agents\meta-top-researcher.md` |
| U4 | `C:\Users\HP\.claude\skills\meta-top\SKILL.md` | `C:\Users\HP\projects\meta-top\skills\meta-top\SKILL.md` |
| U5 | (no file edits; sync-only) | n/a |

## Post-approval next step

Run `/ce-work` with this plan file. `ce-work` should:
1. Execute U1 → U4 in order — each is a single Edit call against the live path
2. Run U5 sync after U1–U4 land (mirror working-copy → live for posterity)
3. Run `ce-code-review` against the changed files (per the 2026-09-27 plan's precedent)
4. Stop and surface results for ship/no-ship decision (no auto-commit per the no-claude-footer rule + scope-discipline rule)

If `ce-work` is unavailable, the same flow can run inline as **4 Edit calls + 1 sync round**, all against the live paths.
