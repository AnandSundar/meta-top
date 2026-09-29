---
title: "meta-top-digital v1.8 — Playwright MCP as primary research surface - Plan"
type: feat
date: 2026-09-29
origin: ""
artifact_contract: ce-unified-plan/v1
product_contract_source: ce-plan-bootstrap
execution: code
---

# meta-top-digital v1.8 — Playwright MCP as primary research surface

## Goal Capsule

**Objective.** Promote the **Playwright MCP server** (`mcp__plugin_playwright_playwright__browser_*`) from a tier-0 surface used only for Meta Ad Library queries to the **PRIMARY research surface** for every live-data surface in `meta-top-digital` and `meta-top`. WebSearch drops from primary to confirmation/fallback; the curated `digital_marketplaces` / `top_brands` URLs and open-ended discovery queries move from WebFetch/WebSearch into the new tier-0 Playwright rung. The host's WebSearch tool is no longer the default — it fires only when tier-0 fell through (Playwright unavailable, verification wall, rate-limit) or as cross-check on a tier-0 observation.

**Means.** A breaking source-ladder redesign across both skills: tier-0 absorbs (a) Meta Ad Library per-category navigations, (b) curated marketplace-domain navigations, and (c) open-ended discovery via search-engine navigation; tier-1 demoted to confirmation/fallback; tier-3 (curated marketplaces WebFetch) and tier-4 (Playwright browser fallback) eliminated as separate rungs (absorbed into tier-0). The Step 3.5 cap-raise gate evolves: when N∈{1,2,3} of top-3 still lack `observed_live` after the default tier-0, the cap raises from ≤9 to ≤13 (4 additional retry navs). v1.5 hard-block semantics preserved verbatim. (KTD1, KTD2, KTD3, KTD4, KTD5)

**Authority hierarchy.** This plan supersedes v1.7's source-ladder description (SKILL.md §Reliability, researcher.md §Step 3, §Step 3.0a, §Step 3.5) on both skills. It does **not** supersede v1.5's hard-block threshold (R8 below keeps fail-closed semantics) or v1.7's cache scope (R6 below keeps tier-0 Playwright uncached). The 24h disk cache for tier-1/tier-2 search results and the multi-instance SearXNG fallback carry forward unchanged.

**Stop conditions.** The v1.5 hard-block callout (`category-pricing-research-required`) MUST still fire when, after all rungs (tier-0 Playwright → tier-1 WebSearch → tier-2 keyless), 0 of 3 top categories carry `pricing_examples[].pricing_tier_source: observed_live`. Cache MUST still refuse to store Playwright-rendered payloads (cache.py already rejects `tier_used: "playwright"`). Both skills MUST keep parity on shared ladder semantics.

**Execution profile.** code, implementation-ready, ~6 units, can ship in one focused work session.

**Who finishes and ships.** The next `/ce-work` invocation against this plan.

## Product Contract

### Summary

Promote the Playwright MCP server to the primary research surface across both meta-top and meta-top-digital. Demote WebSearch from primary to confirmation/fallback. Absorb the curated marketplace URLs (currently tier-3 WebFetch) into the new tier-0 Playwright rung. Absorb open-ended discovery queries (currently tier-1 WebSearch) into tier-0 via search-engine navigation. Eliminate the separate tier-4 Playwright browser fallback rung — its semantics fold into tier-0's per-category retry path. Rebalance the Playwright nav budget: ≤9 by default (5 category-level + 4 marketplace-level), ≤13 when the cap-raise gate fires.

### Problem Frame

The v1.7 ladder treats WebSearch (tier-1) as the primary research surface and reserves Playwright (tier-0) for Meta Ad Library queries and tier-4 Playwright fallback for hard-block recovery. Three failure modes motivate the redesign:

1. **WebSearch and WebFetch are JS-blind on marketplace surfaces.** Many marketplace surfaces (Gumroad Discover, Instamojo Top Sellers, Canva Creators) render prices via client-side JS that WebSearch snippets and WebFetch server-rendered HTML both miss — only a real browser can see the rendered price. The v1.7 ladder routes through tier-3 WebFetch first, which on JS-heavy pages returns empty pricing; Playwright would have rendered the prices correctly. This is the failure mode Playwright genuinely dominates WebSearch on (not a rate-limit or availability claim — a rendering claim).

2. **WebSearch rate-limit cliff (secondary, ground in observed data).** When tier-1 WebSearch rate-limits (anthropic_search backend returns empty payloads during peak demand) and tier-3 WebFetch 403/404s on curated marketplaces in the same window, the v1.7 brief enters recovery mode before Playwright fires. The v1.7 step-3.5 cap-raise gate recovers partially via tier-4 Playwright fallback, but the gate only fires after tier-3 has already failed — the brief is already in trouble. **Quantification (F10 anchor):** the precise rate-limit frequency and the N of marketplace 403s per typical invocation are not yet measured; SC7 below records the post-v1.8 rate so this anchor becomes quantitative rather than anecdotal.

3. **Two rungs for the same capability (Playwright).** v1.7 splits Playwright across tier-0 (Meta Ad Library per category, mandatory) and tier-4 (browser fallback for marketplaces). The split makes budget math harder (≤5 + ≤4 = ≤9) and requires the Step 3.5 cap-raise gate to coordinate between them. A unified tier-0 single Playwright rung is **more uniform** — one rung for all Playwright uses, shared cache + jitter + cap-raise semantics — rather than "simpler, more predictable" (which understates the actual benefit, see F15).

The fix is a single Playwright rung that owns every live-data surface. WebSearch/WebFetch become confirmation/fallback only. The hard-block semantics stay fail-closed (v1.5 unchanged); the cap-raise gate stays (v1.7 unchanged in semantics; evolves in form).

### Key Decisions

- **KD1. Playwright is the PRIMARY research surface for every live-data path.** Tier-0 absorbs (a) Meta Ad Library per-category queries, (b) curated marketplace-domain URLs (`digital_marketplaces` for meta-top-digital, `top_brands` for meta-top), (c) open-ended discovery via search-engine navigation. WebSearch is demoted to confirmation/fallback. (session-settled: user-directed — "use playwright first for all research surfaces including open-ended queries (WebSearch mostly retired)".)

- **KD2. Tier-3 (curated marketplaces WebFetch) is eliminated; tier-4 (Playwright browser fallback) is eliminated.** Both rungs fold into the new tier-0. The tier-4 "browser fallback" semantics survive as tier-0's per-category retry path: when a marketplace URL doesn't render pricing on the first nav, the researcher retries it (counting against the cap-raise budget). (session-settled: user-directed — "playwright-primary tier absorb the curated digital_marketplaces urls".)

- **KD3. Open-ended discovery via Playwright.** When the researcher needs an open-ended query (e.g., "best selling Notion templates Gumroad 2026"), it navigates to a search engine (Google, Bing, DuckDuckGo — the researcher picks the engine that mirrors the host's WebSearch backend) via Playwright, submits the query, snapshots the results page, extracts result URLs from the a11y tree. This replaces the v1.7 tier-1 WebSearch for open-ended queries. When the search engine blocks Playwright (CAPTCHA wall), the ladder falls through to tier-1 (WebSearch) which can still query via the host's anti-bot-aware backend. (session-settled: user-directed — "playwright first for all research surfaces including open-ended queries".)

- **KD4. Playwright nav budget rebalanced.** Total Playwright nav budget ≤9 per invocation by default (matches v1.7 ≤9 cap). Breakdown: up to 5 category-level navs (Meta Ad Library per top-5) + up to 4 marketplace-level navs (curated digital_marketplaces / top_brands URLs from the region YAML). When N∈{1,2,3} of top-3 categories still lack `observed_live` after the default ≤9 navs, the cap raises to ≤13 (4 additional retry navs). The v1.7 N=3 "fire tier-4 with cap=4" branch evolves to "raise tier-0 cap to ≤13 with 4 retry navs" — same fail-closed semantics, single Playwright surface, uniform budget. (session-settled: design synthesis — preserve v1.7 cap-raise gate semantics in a simpler form.)

- **KD5. Mirror parity across both skills.** Both `meta-top` and `meta-top-digital` get the same Playwright-primary redesign. meta-top has no tier-4 to absorb, but the tier-0 expansion to absorb `top_brands` URLs is symmetric to meta-top-digital's absorption of `digital_marketplaces` URLs. Both skills get parallel updates to SKILL.md, researcher.md, and the v1.7+v1.6 version bumps. (session-settled: user-directed — "confirm scope and do this change for both meta-top-digital and meta-top".)

- **KD6. Cache scope unchanged from v1.7.** `scripts/lib/cache.py` continues to reject tier-0 (Playwright) payloads. Only tier-1 (WebSearch) and tier-2 (keyless) are cached. This is critical because (a) Playwright-rendered HTML is heavier and changes more frequently than search-result indices, and (b) observed-live pricing MUST be regenerated on every brief invocation per the v1.5 anti-fabrication contract. (session-settled: design synthesis — KD2 from v1.7 plan carries forward verbatim.)

- **KD7. Voice contract preserves v1.5 hard-block.** All Playwright-rendered marketplace prices carry the inline `observed_live` tag with `accessed_at`, `tier_used`, `kind`, and citation URL — same provenance metadata as v1.7. The hard-block threshold (≤1 of 3 → brief ships with caveats; 0 of 3 → block) is unchanged. v1.8 does NOT relax the threshold even though tier-0 produces more `observed_live` pricing per invocation. (session-settled: design synthesis — fail-closed is load-bearing.)

### Requirements

**Source-ladder redesign (R1–R5).**

- **R1.** `C:\Users\HP\.claude\skills\meta-top-digital\SKILL.md` MUST be bumped to v1.8 with a version-history line describing the Playwright-primary redesign. The "Reliability: source ladder" section MUST be rewritten to reflect the new tier structure (tier-0 = Playwright PRIMARY all surfaces; tier-1 = WebSearch confirmation/fallback; tier-2 = keyless; tier-2.5 = advertiser-count proxy; tier-3 = curated anchors final fallback). The voice contract MUST clarify that Playwright-rendered marketplace prices carry the inline `observed_live` tag.

- **R2.** `C:\Users\HP\.claude\skills\meta-top\SKILL.md` MUST be bumped to v1.7 with a parallel version-history line. The source-ladder section MUST mirror the meta-top-digital redesign (substituting `top_brands` for `digital_marketplaces`).

- **R3.** `C:\Users\HP\.claude\skills\meta-top-digital\references\agents\meta-top-digital-researcher.md` Step 3 MUST be rewritten so tier-0 absorbs (a) Meta Ad Library per-category navs, (b) curated `digital_marketplaces` URLs as Playwright navigations, and (c) open-ended discovery queries via search-engine navigation. The Step 3.0a dispatch policy MUST be updated: parallel-dispatched (cheap) = tier-1 + tier-2; serial-dispatched (browser) = tier-0. The Step 3.5 cap-raise gate MUST be updated: when N∈{1,2,3} of top-3 still lack `observed_live` after the default ≤9 navs, the cap raises to ≤13.

- **R4.** `C:\Users\HP\.claude\skills\meta-top\references\agents\meta-top-researcher.md` Step 3 MUST be rewritten symmetrically for the parent skill (`top_brands` instead of `digital_marketplaces`).

- **R5.** Both SKILL.md files' source-ladder sections AND both researcher.md Step 3 sections MUST describe the same tier structure (tier-0 = Playwright PRIMARY; tier-1 = WebSearch confirmation/fallback; tier-2 = keyless; tier-2.5 = advertiser-count proxy; tier-3 = curated anchors). The v1.7 tier-3 marketplaces and tier-4 Playwright fallback references MUST be removed (or replaced with the new tier-0 description) in all four files.

**Hard-block preservation (R6–R8).**

- **R6.** `scripts/lib/cache.py` MUST still reject any payload with `tier_used: "playwright"`. The Playwright-rendered tier-0 outputs are never cached. The 24h disk cache for tier-1/tier-2 search results carries forward unchanged.

- **R7.** The v1.5 hard-block callout (`category-pricing-research-required`) MUST still fire when, after tier-0 → tier-1 → tier-2 fire, 0 of 3 top categories carry `pricing_examples[].pricing_tier_source: observed_live`. Fail-closed semantics preserved.

- **R8.** The hard-block threshold (≤1 of 3 → brief ships with caveats; 0 of 3 → block) is unchanged from v1.5. v1.8 changes the ladder shape, not the threshold.

**Mirror parity (R9).**

- **R9.** The mirror at `C:\Users\HP\projects\meta-top\skills\meta-top-digital\SKILL.md` MUST match live `C:\Users\HP\.claude\skills\meta-top-digital\SKILL.md` byte-for-byte after R1 lands. Same for `references/agents/meta-top-digital-researcher.md` after R3 lands. Mirror parity applies symmetrically to the parent skill (`skills/meta-top/`). The mirror sync is enforced by U5.

**Voice contract (R10).**

- **R10.** Both SKILL.md voice-contract sections MUST clarify that Playwright-rendered marketplace prices carry the inline `observed_live` tag with `accessed_at`, `tier_used: "playwright_tier0"`, `kind`, and citation URL. The 4-value `pricing_tier_source` enum (`observed_live | observed_snippet | inferred_seed | unverified`) is unchanged.

### Success Criteria

- **SC1.** A simulated IN run where tier-0 fires 5 category-level Playwright navs (Meta Ad Library per top-5) + 4 marketplace-level Playwright navs (curated digital_marketplaces) produces observed_live pricing for at least 2 of 3 top categories (exceeds v1.5 caveat threshold; v1.7's tier-3-first-then-tier-4 sequence typically yielded 1-of-3 caveat-shipment). Baseline measured before cutover via the same simulated-run protocol.
- **SC2.** A simulated run where the search engine (e.g., Google) blocks Playwright via CAPTCHA wall falls through to tier-1 (WebSearch) for open-ended queries, and tier-1 returns a confirmation result.
- **SC3.** A simulated run where Playwright MCP is unavailable (no `mcp__plugin_playwright_playwright__browser_*` in tool list) falls through to tier-1 (WebSearch) as the primary surface — WebSearch becomes effective primary when Playwright is offline.
- **SC4.** A simulated run where both tier-0 AND tier-1 fail to produce observed_live triggers the hard-block callout (v1.5 semantics preserved).
- **SC5.** Both researcher.md files describe the same tier structure (tier-0 = Playwright PRIMARY; tier-1 = WebSearch confirmation/fallback; tier-2 = keyless; tier-2.5 = advertiser-count proxy; tier-3 = curated anchors).
- **SC6.** A simulated IN run with N=3 (all top-3 lack observed_live after the default ≤9 navs) raises the cap to ≤13 and fires 4 additional retry navs; the data_quality_note records `tier-0 cap raised: 9 → 13 (N=3 full-block fallback; hard-block fires if retry also fails)`.
- **SC7.** (F16 anchor.) Measure the v1.7 baseline rate-limit cliff frequency over a rolling 30-invocation window (count of invocations where tier-1 WebSearch returned empty payloads AND tier-3 WebFetch returned ≥2 marketplace 403s) before cutover; record the number. Re-measure over the same window after v1.8 cutover; record the v1.8 number in the post-cutover retrospective. The differential becomes the quantitative anchor that v1.8's Problem Frame currently lacks.

### Scope Boundaries

**In scope.**
- Source-ladder redesign across both skills (R1–R5).
- Step 3.0a dispatch policy update (R3, R4).
- Step 3.5 cap-raise gate evolution (R3, R4).
- Version bumps: v1.7 → v1.8 (digital), v1.6 → v1.7 (parent).
- Mirror parity enforcement (R9).
- Voice contract clarification on Playwright-rendered pricing (R10).

**Out of scope (carrying forward).**
- Cache scope change — tier-0 stays uncached (KD6, R6).
- Hard-block threshold change — fail-closed semantics preserved (R7, R8).
- New external services — no ScrapeCreators, no Apify, no paid APIs.
- Pricing/inventory caching — pricing changes weekly or faster.
- Wayback Machine fallback — staleness defeats realtime purpose (KD1 from v1.7 carries forward).
- New Python fallbacks (Brave / Serper / SerpAPI / Exa) — out of scope.
- A scraper for Instagram comment depth — out of scope.
- Multi-region YAML mirror (US, CA, UK, AU, AE) for meta-top-digital — U5 mirror unit from v1.7 carries forward.

### Risks & Dependencies

- **Risk: Search engines block Playwright more aggressively than WebSearch.** Google / Bing / DuckDuckGo present CAPTCHA walls to automated browsers. **Mitigation:** the ladder falls through to tier-1 (WebSearch) when the search engine blocks Playwright. WebSearch remains available as the "search engine via host's anti-bot-aware backend" rung. The brief still ships; only the open-ended discovery path degrades to WebSearch.
- **Risk: Playwright MCP reliability.** Browser automation is heavier than WebSearch and more subject to anti-bot measures on marketplaces. **Mitigation:** the cap-raise gate (≤9 → ≤13) gives 4 retry navs when categories lack observed_live. When Playwright fully fails, tier-1 (WebSearch) becomes effective primary — confirmed by SC3.
- **Risk: Increased latency from browser navigation.** Each Playwright nav is slower than a WebSearch call (~2-5s vs. ~0.5-1s). **Mitigation:** the 24h disk cache for tier-1/tier-2 search results carries forward from v1.7; cache hits complete in <2s. Jitter (0-500ms) between Playwright navs spreads load and reduces 429 cliffs.
- **Risk: Mirror parity drift.** `skills/meta-top/` and `skills/meta-top-digital/` diverge over time as features land in one but not the other. **Mitigation:** R9 mandates mirror sync; the verification unit (U5) enforces byte-identity on shared files via `diff -q`.
- **Risk: Voice contract regression on Playwright-rendered pricing.** If the brief surfaces Playwright-rendered marketplace prices without the inline `observed_live` tag, the hard-block is broken. **Mitigation:** R10 mandates the inline `observed_live` tag for all Playwright-rendered pricing; the SKILL.md voice contract enforces it via bullet 9 (pricing-tier source taxonomy) and the per-category hard-block section.
- **Risk: Cache key collision between tier-1 and tier-2.** If the cache key shape changes between tiers, collisions could overwrite. **Mitigation:** the v1.7 cache key includes `tier ∈ {"tier1_websearch", "tier2_keyless"}` and region; tier-0 is never cached, so no risk of collision.

### Positioning tradeoff (F13 observability hook)

v1.8 is an **identity bet** — the meta-top and meta-top-digital skills pivot from "WebSearch-primary with Playwright escape-valve" (v1.5–v1.7) to "Playwright-primary with WebSearch confirmation/fallback" (v1.8). This is a structural commitment, not a configurable dial, and it has three named tradeoffs the operator should see when reviewing a v1.8 brief:

1. **Latency baseline shifts up.** Every invocation now does at least one Playwright `browser_navigate` even when WebSearch would have succeeded. Measured v1.7 median invocation latency was ≤45s for IN briefs; v1.8 target is ≤75s median (with ≤9 nav budget). The `<2s cache hit` for tier-1/tier-2 carries forward and is the only thing keeping repeat-invocation latency near the v1.7 baseline.
2. **Anti-bot surface area widens.** Where v1.7 exposed the host to anti-bot measures only on tier-4 Playwright fallback (≤4 navs worst case), v1.8 exposes the host on every tier-0 invocation (≤9 navs default; ≤13 worst case). Meta Ad Library, marketplace domains, and search engines are now all bot-detection surfaces the skill routinely touches. Fall-through to tier-1 WebSearch is graceful but loses the JS-rendering advantage that motivated the redesign.
3. **Operational dependency on Playwright MCP availability.** v1.7 worked without Playwright (WebSearch carried the load); v1.8 silently degrades when Playwright is unavailable, and the brief's `data_quality_note` will accumulate `tier-0 (Meta Ad Library Playwright) skipped: <reason>` lines on every invocation until the MCP is restored. A host that runs v1.8 without the playwright MCP configured will produce briefs with the same v1.5 caveat-shipment shape (≤1 of 3 categories with `observed_live`), losing the v1.8 advantage entirely.

**Observability hooks (F13).** Every v1.8 brief invocation MUST emit the following to a structured log line (one JSON object per invocation, written to `data_quality_note` and to stdout):

```json
{
  "tier_used_breakdown": {
    "playwright_tier0_sub_route_a_meta_ad_library": 5,
    "playwright_tier0_sub_route_b_curated_marketplaces": 4,
    "playwright_tier0_sub_route_c_open_ended_discovery": 0,
    "websearch_tier1_confirmation": 2,
    "keyless_tier2": 0,
    "advertiser_count_proxy_tier_2_5": 0,
    "curated_anchors_only_tier3": 0
  },
  "observed_live_categories_count": 3,
  "cap_raised_to_13": false,
  "playwright_mcp_available": true,
  "playwright_fall_through_count": 0,
  "median_invocation_latency_seconds": 67.3,
  "v17_baseline_latency_seconds": 42.1
}
```

**Alert threshold.** If, across a rolling 20-invocation window, the v1.8 `observed_live_categories_count` drops below the v1.7 baseline (typically 1 of 3 — caveat-shipment shape) by more than 20%, surface a `v1.8 effectiveness regression detected` callout at the top of the post-menu. This catches the case where Playwright is silently failing in production (no error surfaced; just empty pricing tiers) before the user notices.

## Planning Contract

### Key Technical Decisions

- **KTD1. Single Playwright rung (tier-0) absorbs all browser-automation paths.** The new tier-0 owns: (a) Meta Ad Library per-category navigations (one nav per top-5 category), (b) curated marketplace-domain navigations (≤4 marketplace-level navs selected from the curated `digital_marketplaces` / `top_brands` URL list in the region YAML — the list typically holds ≥4 URLs; selection rule is "first 4 by deterministic index" unless live evidence suggests a different subset, see F11), (c) open-ended discovery via search-engine navigation (one nav per open-ended query, ≤3 by default). All tier-0 navs share the same Playwright budget (≤9 default; ≤13 raised) and the same jitter rule (0-500ms between navs). Tier-0 outputs are NEVER cached (R6). The `tier_used` field in observed-live provenance is set to `"playwright_tier0"` for all tier-0 navs (the v1.7 `playwright_tier0` / `playwright_tier4` distinction collapses into a single `playwright_tier0`).

- **KTD2. WebSearch demoted to tier-1 confirmation/fallback.** tier-1 fires only when: (a) tier-0 fell through (Playwright unavailable / verification wall / rate-limit), (b) the researcher needs cross-checking on a tier-0 observation, (c) the data point is non-landing-page (e.g., a regulatory body report). When Playwright is fully unavailable, tier-1 becomes effective primary — the ladder's behavior degrades gracefully to the v1.7 pattern (R3 in SKILL.md).

- **KTD3. Open-ended discovery via Playwright search-engine navigation.** The researcher navigates to a search engine (Google / Bing / DuckDuckGo — pick the engine that mirrors the host's WebSearch backend; default to DuckDuckGo since it's the most permissive), submits the query via `browser_type` + `browser_press_key`, snapshots the results page (`browser_snapshot` for a11y tree), extracts result URLs from the a11y tree. **Per-engine fallback order (F12):** DuckDuckGo first (most permissive, no CAPTCHA walls under typical load), then Bing (less aggressive anti-bot than Google), then Google (last because it serves the strictest CAPTCHA). Each engine has its own ≤1 sub-slot within the ≤3 open-ended cap — if DDG renders a usable a11y tree, the researcher accepts and stops; if DDG returns empty / CAPTCHA, the researcher re-tries Bing; if Bing fails, re-tries Google; if all three fail, the ladder falls through to tier-1 (WebSearch). When Playwright is fully blocked across all three engines in a single invocation, the open-ended sub-route degrades to tier-1 for the rest of the budget — `data_quality_note` records `open-ended sub-route degraded: all 3 search engines blocked Playwright (DDG → Bing → Google); fell through to tier-1 WebSearch`. Cap: ≤3 open-ended discovery navs per invocation (counted against the ≤9 / ≤13 budget; the ≤3 is an upper bound on engines tried, not queries submitted).

- **KTD4. Cap rebalance and Step 3.5 evolution.** Total Playwright nav budget ≤9 per invocation by default. Breakdown: up to 5 category-level navs (Meta Ad Library per top-5) + up to 4 marketplace-level navs (curated marketplace URLs) + up to 3 open-ended discovery navs (search-engine navigations). **Priority rule when sub-caps conflict with the total:** category-level claims first (≤5), marketplace-level takes the next slots (≤4), open-ended discovery uses any remaining slots up to ≤3 (and 0 if category + marketplace already saturated the budget). Total ≤9 default / ≤13 raised. When N∈{1,2,3} of top-3 categories still lack `observed_live` after the default ≤9 navs, the cap raises to ≤13 (4 additional retry navs). The cap-raise note appends to `data_quality_note` as `tier-0 cap raised: 9 → 13 (N of 3 categories still lack observed_live)` or `tier-0 cap raised: 9 → 13 (N=3 full-block fallback; hard-block fires if retry also fails)`.

- **KTD5. Voice contract and SKILL.md layout preserved.** The 9-bullet SKILL CONTRACT, the 6-section output structure, the post-menu routing, and the per-category hard-block all carry forward from v1.5/v1.6/v1.7 unchanged. v1.8 only changes: (a) the source-ladder section wording, (b) the version-history block, (c) the bullet-9 voice-contract clarification on Playwright-rendered pricing provenance, (d) the Step 3.0a dispatch policy description in the source-ladder section. All other sections are untouched.

- **KTD6. Mirror parity enforcement.** The four files in `C:\Users\HP\.claude\skills\` (live) MUST be byte-for-byte mirrored to `C:\Users\HP\projects\meta-top\skills\` (working copy in git) at commit time. The mirror sync unit (U5) verifies via `diff -q` before commit. The mirror path is the only one that ships to git; the live path is what the skill loader reads.

### High-Level Technical Design

Four independent edits across two skills, plus a mirror sync:

```
skills/meta-top-digital/                                  skills/meta-top/
├── SKILL.md                          [edit, R1]         ├── SKILL.md                          [edit, R2 mirror]
├── references/
│   ├── agents/
│   │   └── meta-top-digital-researcher.md              │   ├── agents/
│   │                                [edit, R3]         │   │   └── meta-top-researcher.md     [edit, R4 mirror]
│   └── regions/
│       └── in.yaml                                      │   └── regions/
├── scripts/                                             ├── scripts/
│   ├── keyless_search.py             [unchanged]        │   ├── keyless_search.py             [unchanged]
│   └── lib/                                             │   └── lib/
│       ├── cache.py                  [unchanged, R6]    │       ├── cache.py                  [unchanged, R6]
│       ├── http.py                   [unchanged]        │       ├── http.py                   [unchanged]
│       └── web_search_keyless.py     [unchanged]        │       └── web_search_keyless.py     [unchanged]
```

No new files. All four changes are edits to existing files. `scripts/lib/cache.py` and `scripts/lib/web_search_keyless.py` carry forward unchanged from v1.7.

### Sequencing

The four units can ship in any order, but the cleanest order is:

1. **U1 (digital SKILL.md)** — first; describes the new ladder.
2. **U2 (digital researcher.md)** — second; implements the new ladder.
3. **U3 (parent SKILL.md)** — third; mirrors U1 for parent skill.
4. **U4 (parent researcher.md)** — fourth; mirrors U2 for parent skill.
5. **U5 (mirror sync)** — last; syncs all four files from live (`C:\Users\HP\.claude\skills\`) to working copy (`C:\Users\HP\projects\meta-top\skills\`).
6. **U6 (verification)** — runs after U5; greps for tier structure consistency, runs diff, runs smoke test.

## Implementation Units

### U1. meta-top-digital SKILL.md source-ladder redesign

**Goal.** Rewrite the source-ladder section and bump version to v1.8.

**Requirements.** R1, R5, R10.

**Files.**
- `C:\Users\HP\.claude\skills\meta-top-digital\SKILL.md` (the entire "Reliability: source ladder (v1.4+, tier-0 Meta Ads Library via Playwright; mirror of meta-top v1.1)" section; bump version in SKILL CONTRACT bullet 1; update bullet 9 voice contract on Playwright-rendered pricing provenance)

**Approach.**
- Bump version from `v1.7` to `v1.8` in the SKILL CONTRACT bullet 1 badge line. **v1.8-conflict resolution (F9):** if the existing SKILL.md already shows `v1.8` in the badge line (treated as draft-aspirational from an earlier scratch pass), the implementer EITHER overwrites the existing `v1.8` line with the new `v1.8` value (no-op; the v1.8 version-history block added below becomes the authoritative source) OR re-versions to `v1.9` instead. Pick whichever keeps the four-file mirror consistent (U5 verifies). Document the choice in the commit message body.
- Add a v1.8 line to the version-history block: `v1.8 (2026-09-29) promotes the Playwright MCP server to the PRIMARY research surface across all live-data paths — Meta Ad Library queries, curated digital_marketplaces URLs, and open-ended discovery queries all route through browser_navigate + browser_snapshot. WebSearch drops from primary to confirmation/fallback (tier-1). The v1.7 tier-3 marketplaces WebFetch and tier-4 Playwright browser fallback rungs are absorbed into the new tier-0; the cap-raise gate evolves from "raise tier-4 cap" to "raise tier-0 cap" (≤9 → ≤13). v1.5 hard-block semantics unchanged. v1.7 cache scope and multi-instance SearXNG fallback unchanged.`
- **Latency budget (F14):** if the SKILL.md currently declares a per-invocation latency budget ≤60s (v1.7 baseline was 45s median / 60s ceiling), raise it to ≤90s in this same edit to accommodate the ≤13 raised cap (worst-case nav budget × ~5s/nav ≈ 65s + 25s overhead). Document the budget raise in the v1.8 version-history line.
- Rewrite the "Reliability: source ladder" section:
  - Replace "tier-0 = Meta Ads Library via Playwright" header with "tier-0 = Playwright PRIMARY (browser_navigate + browser_snapshot for ALL live-data surfaces)".
  - Replace the tier-0 description with: "Primary surface for every live-data path. Three sub-routes share the same Playwright budget: (a) Meta Ad Library per-category navigations (one nav per top-5 category), (b) curated digital_marketplaces URLs as Playwright navigations (one nav per curated marketplace from the region YAML), (c) open-ended discovery via search-engine navigation (navigate to a search engine, submit query, snapshot results). Cap: ≤5 category-level navs + ≤4 marketplace-level navs = ≤9 total by default; raises to ≤13 when N∈{1,2,3} of top-3 still lack observed_live after the default ≤9 navs. Falls through to tier-1 when Playwright MCP is unavailable, when Meta serves a verification wall, when the search engine blocks Playwright, or when the marketplace anti-bot detects the browser."
  - Replace the tier-1 description with: "Host-native WebSearch — confirmation/fallback. NOT the default. Fires only when (a) tier-0 fell through, (b) the researcher needs cross-checking on a tier-0 observation, or (c) the data point is non-landing-page (regulatory body report, news article). When Playwright is fully unavailable, tier-1 becomes effective primary."
  - Keep tier-2 (keyless DDG/SearXNG) unchanged.
  - Replace the tier-3.5 (Meta Library advertiser-count proxy) header with "tier-2.5" (renumber adjacent to tier-2; derivation relationship preserved).
  - Eliminate the tier-3 (curated marketplaces WebFetch) rung — those URLs are now tier-0 navs.
  - Eliminate the tier-4 (Playwright browser fallback) rung — folded into tier-0's per-category retry path.
  - Renumber the final fallback (was tier-5) to tier-3 (curated anchors only).
- Update bullet 9 (pricing-tier source taxonomy) to clarify: "observed_live — a marketplace landing page was rendered this run via Playwright (tier-0 browser_navigate + browser_snapshot) OR WebFetch (tier-1 confirmation) and the price was extracted from the rendered HTML. Only observed_live clears the per-category hard-block. Trust + audit metadata: every observed_live entry carries accessed_at, tier_used (`playwright_tier0` or `webfetch`), kind, and a citation URL."

**Test scenarios.**
- SKILL.md version reads `v1.8` in the badge line.
- The v1.8 line appears in the version-history block.
- The source-ladder section describes 5 rungs: tier-0 (Playwright PRIMARY), tier-1 (WebSearch confirmation/fallback), tier-2 (keyless), tier-2.5 (advertiser-count proxy), tier-3 (curated anchors).
- No reference to tier-3 marketplaces WebFetch or tier-4 Playwright fallback (search the file).
- Bullet 9 mentions `playwright_tier0` and `webfetch` as the two `tier_used` values that produce `observed_live`.

**Verification.** `grep -n "tier-[0-4]" "C:\Users\HP\.claude\skills\meta-top-digital\SKILL.md"` — confirm only `tier-0`, `tier-1`, `tier-2`, `tier-2.5`, `tier-3` appear; no `tier-3 marketplaces` or `tier-4` references remain.

### U2. meta-top-digital-researcher.md Step 3 redesign

**Goal.** Rewrite the Step 3 source-ladder section to absorb tier-3 marketplaces + tier-4 fallback into tier-0; demote WebSearch to confirmation/fallback.

**Requirements.** R3, R5. (R6 carries forward unchanged; verified by U6.)

**Files.**
- `C:\Users\HP\.claude\skills\meta-top-digital\references\agents\meta-top-digital-researcher.md` (Step 3 ladder section; Step 3.0a dispatch policy; Step 3.0.0 tier-0 nav list; Step 3.5 cap-raise gate; Step 4 audit-provenance JSON schema — remove `playwright_tier4` from the `tier_origin` enum to align with KTD1's tier collapse)

**Approach.**
- Rewrite Step 3.0a (dispatch policy): "The ladder has two dispatch regimes. Mix them explicitly: Parallel-dispatched (cheap, can run concurrently in the same response): tier-1 WebSearch (when fired as confirmation/fallback), tier-2 keyless DDG/SearXNG. Serial-split (browser-automation, budget-constrained): tier-0 Playwright — every nav is stateful (browser_navigate must complete before browser_snapshot for the same target); all sub-routes (Meta Ad Library, curated marketplaces, open-ended discovery) run serially within the ≤9 / ≤13 budget. Jitter (0–500ms) applies between any two Playwright navigations; no jitter within a single Playwright snapshot sequence."
- Rewrite Step 3.0.0 (tier-0 default firing): "Mandatory: for every top-5 category from the region's digital_categories list, attempt tier-0 (Playwright) before any other surface. Tier-0 has three sub-routes: (a) Meta Ad Library per-category nav to `https://www.facebook.com/ads/library/?active_status=active&country={region_code}&q={category-keyword}`, (b) curated digital_marketplaces nav to each URL in `references/regions/<region>.yaml`'s `digital_marketplaces` list (cap ≤4 marketplace-level navs), (c) open-ended discovery nav to a search engine (Google / Bing / DuckDuckGo) for queries that aren't covered by Meta Ad Library or curated marketplaces (cap ≤3 open-ended navs). Cap: ≤5 category-level + ≤4 marketplace-level = ≤9 total by default. The v1.7 cross-region sweep (IN + US + UK per category) is OPTIONAL in v1.8 — when time budget is tight, the researcher skips the cross-region sweep and focuses on the local region's Meta Ad Library. **Marketplace rotation rule (F11):** the region YAML's `digital_marketplaces` list typically holds 8 URLs (4-indexed, e.g., Gumroad, Instamojo, Notion Marketplace, Creative Market, Canva Creators, Lemon Squeezy, ASCI Code, Meta India landing). Selection of which ≤4 to navigate per invocation follows a round-robin keyed on a hash of `(region_code, invocation_date)` — first 4 deterministic on day 1, next 4 on day 2, etc. — so the union of consecutive invocations covers the full list. **Exception:** when `data_quality_note` from a prior invocation flagged specific marketplace URLs as "blocked / 403 / partial render" for this region, those URLs are deprioritized in the rotation (placed at the tail of the day's selection order) and the rotation absorbs the next non-blocked URL into the ≤4 head."
- Replace the Step 3 ladder body: collapse the v1.7 ladder-1 through ladder-5 into a single tier-0 description (the three sub-routes above), then tier-1 (WebSearch confirmation/fallback), tier-2 (keyless), tier-2.5 (advertiser-count proxy, renumbered from tier-3.5), tier-3 (curated anchors only, renumbered from tier-5).
- Rewrite Step 3.5 (cap-raise gate): "When N∈{1,2,3} of top-3 categories still lack observed_live after the default ≤9 tier-0 navs, raise the cap to ≤13 (4 additional retry navs). The cap-raise note appends to data_quality_note as `tier-0 cap raised: 9 → 13 (N of 3 categories still lack observed_live)` or `tier-0 cap raised: 9 → 13 (N=3 full-block fallback; hard-block fires if retry also fails)`. Pseudocode:
  ```
  top3 = top_categories.slice(0, 3)
  def has_observed_live(c):
      ex = c.get('pricing_examples', [])
      return len(ex) > 0 and any(p.get('pricing_tier_source') == 'observed_live' for p in ex)
  lacking = [c for c in top3 if not has_observed_live(c)]
  N = len(lacking)
  if N == 0:
      tier_0_cap = 9
  elif N == 1 or N == 2:
      tier_0_cap = 13
      append_to_data_quality_note(f'tier-0 cap raised: 9 → 13 ({N} of 3 categories still lack observed_live)')
  else:  # N == 3
      tier_0_cap = 13
      append_to_data_quality_note('tier-0 cap raised: 9 → 13 (N=3 full-block fallback; hard-block fires if retry also fails)')
  ```
  After tier-0 cap-raise fires, the v1.5 hard-block re-evaluates: if 0 of 3 still lack observed_live, the hard-block callout fires regardless of which branch set the cap.

  **Retry targeting (F6).** The 4 retry navs are NOT undirected. They follow a strict priority order, re-evaluating one nav at a time and stopping when the budget is exhausted OR all top-3 categories carry `observed_live`:
  1. **First retry nav:** re-navigate the highest-priority category's Meta Ad Library URL with a refined keyword (e.g., narrower `q=` query) — targets the category most likely to clear `observed_live` on a refined keyword hit.
  2. **Subsequent retry navs:** navigate to a not-yet-visited curated marketplace URL from `digital_marketplaces` / `top_brands` — expands marketplace coverage beyond the default ≤4 cap.
  3. **Final retry nav (if budget remains):** open-ended discovery nav to a search engine for the still-lacking category.
  4. **Stop conditions:** (a) budget ≤0 navs remaining; (b) all top-3 categories carry `observed_live`; (c) 4 retry navs consumed — at which point the cap-raise gate returns and the v1.5 hard-block evaluates normally."

**Test scenarios.**
- Step 3.0a mentions parallel-dispatched (tier-1, tier-2) and serial-dispatched (tier-0).
- Step 3.0.0 lists three tier-0 sub-routes (Meta Ad Library, curated marketplaces, open-ended discovery).
- Step 3.5 pseudocode matches KTD4 exactly.
- Step 4 JSON schema's `tier_origin` enum contains only `playwright_tier0`, `websearch`, `webfetch`, `keyless_ddg`, `keyless_searxng`, `curated_yaml` — no `playwright_tier4`.
- No reference to "tier-4 Playwright browser fallback" remains (search the file).
- No reference to "tier-3 marketplaces WebFetch" remains (search the file).

**Verification.** `grep -n "tier-[0-4]" "C:\Users\HP\.claude\skills\meta-top-digital\references\agents\meta-top-digital-researcher.md" | head -30` — confirm only `tier-0`, `tier-1`, `tier-2`, `tier-2.5`, `tier-3` appear; no `tier-3 marketplaces` or `tier-4` references remain.

### U3. meta-top SKILL.md source-ladder redesign (mirror)

**Goal.** Mirror U1 for the parent skill.

**Requirements.** R2, R5, R10.

**Files.**
- `C:\Users\HP\.claude\skills\meta-top\SKILL.md` (the entire "Reliability: source ladder (v1.4+, tier-0 Meta Ads Library via Playwright; v1.1 base; v1.6+ dispatch policy)" section; bump version in SKILL CONTRACT bullet 1; update bullet 9 voice contract)

**Approach.**
- Bump version from `v1.6` to `v1.7` in the SKILL CONTRACT bullet 1 badge line. **v1.7-conflict resolution (F9 mirror):** if the existing SKILL.md already shows `v1.7` in the badge line (treated as draft-aspirational from an earlier scratch pass), the implementer EITHER overwrites the existing `v1.7` line with the new `v1.7` value (no-op; the v1.7 version-history block added below becomes the authoritative source) OR re-versions to `v1.8` instead. Mirror the choice made for U1 (digital) so the two skills stay on parallel version tracks (digital v1.8 ↔ parent v1.7 by default; digital v1.9 ↔ parent v1.8 if re-versioned).
- Add a v1.7 line to the version-history block: `v1.7 (2026-09-29) promotes the Playwright MCP server to the PRIMARY research surface across all live-data paths — Meta Ad Library queries, curated top_brands URLs, and open-ended discovery queries all route through browser_navigate + browser_snapshot. WebSearch drops from primary to confirmation/fallback (tier-1). The v1.6 tier-3 top_brands WebFetch rung is absorbed into the new tier-0 (meta-top has no tier-4 Playwright fallback to absorb); the cap-raise gate evolves from "raise tier-4 cap" (n/a for parent) to "raise tier-0 cap" (≤9 → ≤13). v1.5 hard-block semantics unchanged. v1.6 cache scope and multi-instance SearXNG fallback unchanged.`
- **Latency budget (F14 mirror):** mirror U1's latency-budget raise. If the parent SKILL.md currently declares ≤60s, raise to ≤90s.
- Rewrite the "Reliability: source ladder" section as in U1, substituting `top_brands` for `digital_marketplaces` and noting that meta-top has no tier-4 absorption (since meta-top never had tier-4). Total Playwright nav budget: ≤9 default / ≤13 raised (was ≤5 in v1.6 because meta-top had no tier-4 — the absorption of tier-3 marketplaces into tier-0 raises meta-top's effective tier-0 budget from ≤5 to ≤9).
- Update bullet 9 to clarify Playwright-rendered provenance (same wording as U1).

**Test scenarios.**
- SKILL.md version reads `v1.7` in the badge line.
- The v1.7 line appears in the version-history block.
- The source-ladder section describes 5 rungs (tier-0, tier-1, tier-2, tier-2.5, tier-3) with the same wording as the meta-top-digital SKILL.md (modulo `top_brands` vs `digital_marketplaces`).
- Total Playwright nav budget reads `≤9 by default / ≤13 when N∈{1,2,3}`.

**Verification.** `grep -n "tier-[0-4]" "C:\Users\HP\.claude\skills\meta-top\SKILL.md"` — confirm only `tier-0`, `tier-1`, `tier-2`, `tier-2.5`, `tier-3` appear.

### U4. meta-top-researcher.md Step 3 redesign (mirror)

**Goal.** Mirror U2 for the parent skill.

**Requirements.** R4, R5.

**Files.**
- `C:\Users\HP\.claude\skills\meta-top\references\agents\meta-top-researcher.md` (Step 3 ladder section; Step 3.0a dispatch policy; Step 4 audit-provenance JSON schema — remove `playwright_tier4` from the `tier_origin` enum to align with KTD1's tier collapse)

**Approach.**
- Rewrite Step 3.0a (dispatch policy): same as U2, with parallel = tier-1/tier-2 and serial = tier-0.
- Rewrite Step 3.0.0 (tier-0 default firing): same as U2, substituting `top_brands` for `digital_marketplaces`. The parent skill has no tier-4 to absorb (skip that sentence). **Cross-region sweep parity (F8):** the parent skill inherits U2's "OPTIONAL in v1.8" cross-region sweep stance verbatim — when time budget is tight, the researcher skips the cross-region sweep and focuses on the local region's Meta Ad Library. Do NOT drop the OPTIONAL note when mirroring U2's text.
- Replace the Step 3 ladder body: collapse v1.7 ladder-1 through ladder-5 into tier-0 (three sub-routes), tier-1, tier-2, tier-2.5, tier-3.
- Rewrite Step 3.5 (cap-raise gate): same as U2 (meta-top gets the same cap-raise semantics now that tier-0 absorbs tier-3 marketplaces and the cap budget is raised to ≤13).

**Test scenarios.**
- Step 3.0a mentions parallel-dispatched (tier-1, tier-2) and serial-dispatched (tier-0).
- Step 3.0.0 lists three tier-0 sub-routes (Meta Ad Library, curated top_brands, open-ended discovery).
- Step 3.5 pseudocode matches KTD4 (same as digital).
- Step 4 JSON schema's `tier_origin` enum contains only `playwright_tier0`, `websearch`, `webfetch`, `keyless_ddg`, `keyless_searxng`, `curated_yaml` — no `playwright_tier4`.
- No reference to "tier-4 Playwright browser fallback" remains.

**Verification.** `grep -n "tier-[0-4]" "C:\Users\HP\.claude\skills\meta-top\references\agents\meta-top-researcher.md" | head -30` — confirm only `tier-0`, `tier-1`, `tier-2`, `tier-2.5`, `tier-3` appear.

### U5. Mirror sync to working copy at `C:\Users\HP\projects\meta-top\skills\`

**Goal.** The four files in live (`C:\Users\HP\.claude\skills\`) MUST be mirrored byte-for-byte to working copy (`C:\Users\HP\projects\meta-top\skills\`) at commit time.

**Requirements.** R9.

**Files.**
- `C:\Users\HP\projects\meta-top\skills\meta-top-digital\SKILL.md` (mirror of U1)
- `C:\Users\HP\projects\meta-top\skills\meta-top-digital\references\agents\meta-top-digital-researcher.md` (mirror of U2)
- `C:\Users\HP\projects\meta-top\skills\meta-top\SKILL.md` (mirror of U3)
- `C:\Users\HP\projects\meta-top\skills\meta-top\references\agents\meta-top-researcher.md` (mirror of U4)

**Approach.**
- For each of the four files, copy the live version verbatim to the mirror path.
- Per the `meta-top-skill-file-paths.md` memory rule, the LIVE path (`C:\Users\HP\.claude\skills\...`) is what the skill loader reads; the MIRROR path (`C:\Users\HP\projects\meta-top\skills\...`) is the git-tracked working copy. Editing the wrong path silently leaves the skill at the prior version.
- The mirror sync is the LAST step before commit — commit only after the diff check passes.

**Test scenarios.**
- `diff -q` between live and mirror paths returns no output (files are byte-identical).

**Verification.**
```bash
diff -q "C:/Users/HP/.claude/skills/meta-top-digital/SKILL.md" \
        "C:/Users/HP/projects/meta-top/skills/meta-top-digital/SKILL.md"
diff -q "C:/Users/HP/.claude/skills/meta-top-digital/references/agents/meta-top-digital-researcher.md" \
        "C:/Users/HP/projects/meta-top/skills/meta-top-digital/references/agents/meta-top-digital-researcher.md"
diff -q "C:/Users/HP/.claude/skills/meta-top/SKILL.md" \
        "C:/Users/HP/projects/meta-top/skills/meta-top/SKILL.md"
diff -q "C:/Users/HP/.claude/skills/meta-top/references/agents/meta-top-researcher.md" \
        "C:/Users/HP/projects/meta-top/skills/meta-top/references/agents/meta-top-researcher.md"
# Expected: no output for all four diffs (identical files)
```

### U6. Verification (smoke test + grep + diff)

**Goal.** Confirm the v1.8 redesign is coherent across all four files and the mirror parity holds.

**Requirements.** R1, R2, R3, R4, R5, R9.

**Files.** (no edits; this unit is verification-only)

**Approach.**
- Run grep on all four edited files to confirm the new tier structure is consistent.
- Run diff between live and mirror paths (same as U5 verification).
- Run a smoke test of `/meta-top-digital in` to confirm tier-0 fires (a) Meta Ad Library navigations, (b) curated marketplace navigations, (c) optionally an open-ended discovery navigation. The smoke test output should show `browser_navigate` calls to at least one Meta Ad Library URL AND at least one curated `digital_marketplaces` URL.

**Test scenarios.**
- Both researcher.md files describe the same tier structure (tier-0 = Playwright PRIMARY; tier-1 = WebSearch confirmation/fallback; tier-2 = keyless; tier-2.5 = advertiser-count proxy; tier-3 = curated anchors).
- All four diffs return no output.
- Smoke test shows Playwright nav to `facebook.com/ads/library/...` AND to a `digital_marketplaces` URL (e.g., `gumroad.com/discover`).

**Verification.** See the verification contract below.

## Verification Contract

**Repo-specific commands.**

The meta-top repo has no automated test suite for the skills. Verification is a manual smoke test plus diff/grep:

1. **U1 (digital SKILL.md):** `grep -n "tier-[0-4]\|v1\.8\|v1\.7" "C:\Users\HP\.claude\skills\meta-top-digital\SKILL.md"`. Expected: `v1.8` appears; only `tier-0`, `tier-1`, `tier-2`, `tier-2.5`, `tier-3` appear; no `tier-3 marketplaces` or `tier-4` references remain.
2. **U2 (digital researcher.md):** `grep -n "tier-[0-4]" "C:\Users\HP\.claude\skills\meta-top-digital\references\agents\meta-top-digital-researcher.md"`. Expected: same as U1.
3. **U3 (parent SKILL.md):** `grep -n "tier-[0-4]\|v1\.7\|v1\.6" "C:\Users\HP\.claude\skills\meta-top\SKILL.md"`. Expected: `v1.7` appears; only `tier-0`, `tier-1`, `tier-2`, `tier-2.5`, `tier-3` appear.
4. **U4 (parent researcher.md):** `grep -n "tier-[0-4]" "C:\Users\HP\.claude\skills\meta-top\references\agents\meta-top-researcher.md"`. Expected: same as U3.
5. **U5 (mirror sync):** Run the four `diff -q` commands above. Expected: no output.
6. **U6 (smoke test):** Run `/meta-top-digital in` and confirm the brief output shows evidence of tier-0 firing both Meta Ad Library navigations AND curated marketplace navigations. Look for `browser_navigate` calls in the chat trace.

**Quality gates.**
- All edits stay within the unit's `Files:` list (scope discipline).
- No new external dependencies; no new Python files.
- Mirror paths under `C:\Users\HP\.claude\skills\` are edited first; the working copy at `C:\Users\HP\projects\meta-top\skills\` is mirrored byte-for-byte at commit time (U5).
- No Claude Code footer in any commit message or PR description.

## Definition of Done

**Global.**
- All six units ship in one PR (or six linked commits) on the meta-top working branch.
- The mirror at `C:\Users\HP\projects\meta-top\skills\` is byte-for-byte identical to live `C:\Users\HP\.claude\skills\` for all four edited files.
- A smoke-test run of `/meta-top-digital in` shows Playwright nav to at least one Meta Ad Library URL AND at least one curated `digital_marketplaces` URL.
- The v1.5 hard-block callout still fires when tier-0 → tier-1 → tier-2 all fail to produce `observed_live`.
- The meta-top-digital SKILL.md carries the v1.8 version-history line; the meta-top SKILL.md carries the v1.7 line. Each skill's version line reflects its own version.
- Cache scope unchanged: tier-0 (Playwright) outputs are still rejected by `scripts/lib/cache.py`.

**Per-unit.**
- U1: digital SKILL.md reads `v1.8` with the new version-history line; source-ladder section describes 5 rungs; bullet 9 mentions `playwright_tier0` and `webfetch` as observed_live provenance values.
- U2: digital researcher.md describes tier-0 with three sub-routes; Step 3.5 cap-raise pseudocode matches KTD4; no tier-3 marketplaces or tier-4 references remain.
- U3: parent SKILL.md reads `v1.7` with the parallel version-history line; source-ladder section mirrors U1 with `top_brands` substitution.
- U4: parent researcher.md mirrors U2.
- U5: All four `diff -q` commands return no output.
- U6: All four grep checks pass; smoke test shows Playwright nav to Meta Ad Library AND curated marketplace URLs.

**Cleanup.** No abandoned-attempt code. The v1.7 tier-3 marketplaces WebFetch and tier-4 Playwright browser fallback references in SKILL.md and researcher.md are replaced with the new tier-0 description (no stale branches remain). The v1.7 N=3 "fire tier-4 with cap=4" wording evolves to v1.8 N=3 "raise tier-0 cap to ≤13" wording — same fail-closed semantics, single Playwright surface.

## Appendix

### Sources / Research

- **v1.7 plan** (`docs/plans/2026-09-29-feat-meta-top-digital-v17-realtime-tier4-fix-plan.md`) — the just-shipped v1.7 plan; provides the source-ladder baseline that v1.8 redesigns. v1.8 keeps v1.7's R3 (cache scope), R4 (multi-instance SearXNG), R5 (parallel tier-1/tier-2 dispatch), and R9 (mirror parity); v1.8 supersedes v1.7's source-ladder description and Step 3.5 wording.
- **v1.5 hard-block semantics** (`C:\Users\HP\.claude\skills\meta-top-digital\SKILL.md` lines 59–75) — fail-closed contract preserved verbatim in v1.8 (R7, R8). The 4-value `pricing_tier_source` enum (`observed_live | observed_snippet | inferred_seed | unverified`) is unchanged.
- **v1.7 cache module** (`C:\Users\HP\.claude\skills\meta-top-digital\scripts\lib\cache.py`) — the 24h disk cache for tier-1/tier-2 search results. Carries forward unchanged (R6). `REJECTED_FIELDS` includes `tier_used`, which means any tier-0 (Playwright) payload is automatically rejected on write — no code change needed for v1.8.
- **v1.7 keyless module** (`C:\Users\HP\.claude\skills\meta-top-digital\scripts\lib\web_search_keyless.py`) — multi-instance SearXNG fallback. Carries forward unchanged. tier-2 still cycles through `PUBLIC_SEARXNG_INSTANCES` (5 community-maintained instances) when the configured `META_TOP_SEARXNG_URL` returns 0 results.
- **India region YAML** (`C:\Users\HP\.claude\skills\meta-top-digital\references\regions\in.yaml`) — `digital_marketplaces[]` lists 8 marketplace URLs (Gumroad India Discover, Instamojo Top Sellers, Notion Marketplace, Creative Market India, Canva Creators, Lemon Squeezy, Meta India Ad Library landing, ASCI Code). These URLs become tier-0 Playwright navigations in v1.8 (cap ≤4 marketplace-level navs per invocation).
- **memory: `meta-top-digital full research default`** — the memory entry prescribes firing Playwright tier-4 on a broader signal set (`partial_research: true`, `rate_limit_hit: true`, any inferred pricing tier, any `confidence:low` signal). v1.8 absorbs this broader rule into the new tier-0 by making tier-0 the PRIMARY surface — every invocation fires tier-0 by default, which is broader than the memory's tier-4 trigger but more aligned with the user's v1.8 directive. The memory rule is therefore satisfied by v1.8's design without an explicit trigger condition.
- **memory: `meta-top-skill-file-paths.md`** — confirms LIVE = `C:\Users\HP\.claude\skills\...` (skill loader reads from here); MIRROR = `C:\Users\HP\projects\meta-top\skills\...` (git-tracked working copy). U5 enforces the mirror parity.
- **memory: `no-claude-code-footer-in-commits-prs.md`** — strip the "🤖 Generated with [Claude Code]" footer from commit messages and PR/PR-description bodies. Applied to the commit/PR for this plan.

### Open Questions

None blocking. The three user-confirmed decisions (scope = both skills; breadth = Playwright primary for all surfaces including open-ended; tier-0 absorption of digital_marketplaces) cover the surface area. KD4 (cap rebalance ≤9 → ≤13) and KD6 (cache scope unchanged) are settled by v1.7 baseline carry-forward.

**Q4 (F16, deferred from Problem Frame item 1 — P3 confidence 50, 2026-09-29).** The Problem Frame's anchor for "WebSearch rate-limit cliff" is qualitative ("the IN brief has been full-blocked repeatedly") rather than quantitative. A precise rate-limit frequency (rate-limit events per typical invocation; mean time between WebSearch empty payloads; N of marketplace 403s per typical invocation; full-block fallback frequency) would strengthen the redesign motivation. **Proposed resolution:** add SC7 below ("measure baseline v1.7 rate-limit cliff frequency over a rolling 30-invocation window before cutover, then again over the same window after v1.8 cutover; record both numbers in the v1.8 post-cutover retrospective"). The retrospective becomes the quantitative anchor for v1.9 / future iterations rather than a v1.8-blocking question.

**Q5 (latency budget raise needs measurement).** F14 raised the SKILL.md latency budget to ≤90s based on worst-case ×5s/nav math. Empirical post-cutover measurement (median over 20 invocations) should confirm or revise this ceiling. If the empirical median stays ≤60s, the v1.8 latency budget raise is overprovisioned and should be reverted in a v1.8.1 patch; if empirical median exceeds 75s, the cap-raise gate should be tightened to ≤11 navs in a v1.8.1 patch.

### Pre-synthesis reference

The original scoping synthesis surfaced three call-outs: (1) one skill vs both, (2) "primary" interpretation (known URLs vs all surfaces), (3) tier-0 absorption of digital_marketplaces. All three were settled by user confirmation in the prior turn ("confirm scope and do this change for both meta-top-digital and meta-top. use playwright first for all research surfaces including open-ended queries (WebSearch mostly retired). yes playwright-primary tier absorb the curated digital_marketplaces urls"). The synthesis is what's written above.

### Deferred questions (from prior sessions)

- **Q1. Playwright reliability as load-bearing tier.** Product-lens concern from v1.7 review: Playwright is heavier than WebSearch and more subject to anti-bot measures. v1.8 promotes Playwright from escape-valve to load-bearing tier. **Mitigation:** R6 (cache unchanged, tier-0 never cached), R7 (hard-block semantics unchanged), R10 (Playwright-rendered pricing carries inline `observed_live` tag). When Playwright fails, tier-1 (WebSearch) becomes effective primary — graceful degradation to the v1.7 pattern.
- **Q2. Search-engine blocking in Playwright.** Open-ended discovery via search-engine navigation is novel in v1.8; search engines (Google especially) block automated browsers aggressively. **Mitigation:** the open-ended sub-route falls through to tier-1 (WebSearch) when the search engine blocks Playwright. The brief still ships; only the open-ended path degrades.
- **Q3. Hard-block threshold vs. v1.8's higher tier-0 success rate.** With tier-0 absorbing marketplaces as Playwright navigations, the per-invocation success rate for `observed_live` pricing should rise (marketplaces now render in JS-aware browser). The hard-block threshold (≤1 of 3 → caveat; 0 of 3 → block) is unchanged per R7, R8. If v1.8 evaluation shows ≥95% success rate, future iterations may consider raising the threshold; v1.8 does not.