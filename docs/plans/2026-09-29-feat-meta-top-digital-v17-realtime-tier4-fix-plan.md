---
title: "meta-top-digital v1.7 — Live-data amplification for full-block recovery - Plan"
type: feat
date: 2026-09-29
origin: ""
artifact_contract: ce-unified-plan/v1
product_contract_source: ce-plan-bootstrap
execution: code
---

# meta-top-digital v1.7 — Live-data amplification for full-block recovery

## Goal Capsule

**Objective.** A `/meta-top-digital <region>` invocation in a thin-data region (IN today; CA / UK / AU / AE once U6 mirror ships) recovers from the recurring WebSearch rate-limit + tier-3 marketplace WebFetch 403/404 failure modes without regressing on the v1.5 anti-fabrication hard-block. The brief ships with at least one `observed_live` pricing example per top-3 category wherever the host's Playwright MCP server can render a marketplace surface; when no surface renders, the v1.5 hard-block callout still fires (fail-closed preserved).

**Means.** Six changes: Step 3.5 cap-raise logic lets tier-4 fire in N=3, tier-0 expands from top-3 to top-5, a 24-hour disk cache layer covers only tier-1/tier-2 search-result payloads (NOT pricing or inventory), the tier-2 keyless rung cycles through 3–5 public SearXNG instances before giving up, parallel tier dispatch shortens wall-clock, and the meta-top sibling stays in lockstep for shared modules. (KTD1, KTD2, KTD3, KTD4, KTD5)

**Authority hierarchy.** This plan supersedes v1.6's source-ladder description on the Step 3.5 N=3 branch and on the tier-0 cap. It does **not** supersede v1.5's hard-block threshold (R7 below keeps fail-closed semantics).

**Stop conditions.** v1.5's hard-block callout must still fire when 0 of 3 categories carry `observed_live` after tier-4 fires. Cache must never serve a `pricing_examples` entry — only search-result URLs, snippet text, and source metadata. Mirror at `skills/meta-top/` must keep parity for shared modules.

**Execution profile.** code, implementation-ready, ~6 units, can ship in one focused work session.

**Who finishes and ships.** The next `/ce-work` invocation against this plan.

## Product Contract

### Summary

Add a live-data amplification layer to meta-top-digital that lets Playwright (realtime, JS-rendered, anti-bot-aware) carry more of the load when WebSearch rate-limits and tier-3 WebFetch fails. Six small changes, no schema overhaul, no contract changes for callers, no new external services.

### Problem Frame

The IN brief has been full-blocked repeatedly because tier-1 WebSearch returns empty (rate-limit) and tier-3 marketplace WebFetch returns 403/404/empty for 5 of 6 URLs. The v1.5 hard-block requires `observed_live` pricing for at least 2 of 3 top categories before the brief can ship, so a single rate-limited run collapses to a `category-pricing-research-required` callout with no actionable output. The previous round of proposed fixes (Wayback Machine + snapshot cache + disk cache) makes the research stale by 6–12 months on pricing — defeating the skill's purpose of finding a **current** winning product.

The fix is to amplify realtime signal: make Playwright do more work, gate the cache to slow-moving data only (search-result payloads, not pricing/inventory), and add redundancy at the keyless-search rung. This preserves the skill's realtime identity while raising the recovery rate from rate-limited inputs.

### Key Decisions

- **KD1. No Wayback Machine fallback.** Wayback snapshots are 6–12 months stale on pricing; the skill exists to surface the **current** winning product, so a stale snapshot defeats the purpose. (session-settled: user-directed — chosen over `<Wayback + snapshot cache as primary fix>`: user observed that staleness makes cache wrong answer for "find the current winning product.")
- **KD2. Cache applies to search-result payloads only.** 24-hour disk cache covers tier-1 (WebSearch result URLs + snippet text) and tier-2 (DDG/SearXNG result URLs + snippet text). Never to `pricing_examples`, `underground_signals`, `winning_score`, or any tier-0/tier-4 Playwright observation. Search results are slow-moving relative to inventory; pricing changes weekly or faster. (session-settled: user-directed — chosen over `<cache everything for 24h>`: pricing/inventory staleness would defeat anti-fabrication contract.)

  **Reconciliation with user pushback.** The user categorically rejected disk caches for pricing/inventory in pre-synthesis: *"I want realtime research done to gather data to find the winning product. disk cache, wayback machine, etc will make the research outdated. wont it?"* KD2 narrows the cache to search-result *index* data — list of `{url, title, snippet}` dicts that say WHERE to look — never to the data the brief ships. The cache accelerates the search step (SC2: <2s vs. ~15–30s); realtime pricing is regenerated on every brief via tier-0/tier-4 Playwright (R1, R2, R7). The cache does NOT identify the winning product; tier-0/tier-4 still does that on every invocation. Cached search results only let the researcher find the right marketplace URL faster.
- **KD3. Step 3.5 raises tier-4 cap to 4 even when N=3.** When all 3 of the top categories lack `observed_live` after tier-3, tier-4 fires with cap=4 in an attempt to clear the hard-block via Playwright. If tier-4 also fails to produce `observed_live` for any of the 3, the v1.5 hard-block callout still fires — fail-closed is preserved, only the path to the block changes. (session-settled: user-directed — chosen over `<keep N=3 as "do not fire tier-4">`: prior behavior short-circuited recovery on the only path that could clear the block.)
- **KD4. Mirror parity on shared modules.** The 24h cache layer, multi-instance SearXNG fallback, and parallel tier firing apply to both `meta-top-digital` and `meta-top`. The Step 3.5 logic revision and tier-0 expansion are meta-top-digital-only (meta-top's tier-0 is already a single mandatory Playwright nav per top category; meta-top has no tier-4). (session-settled: user-directed — chosen over `<digital-only fix>`: the same inputs hit the same failure modes in the meta-top ladder.)
- **KD5. Tier-0 expansion to top-5 (not "all categories").** Live pricing research has to stay within the ≤9 Playwright nav budget (≤5 tier-0 + ≤4 tier-4). Top-5 covers the typical `top_categories` size for v1 regions while leaving headroom for tier-4 to clear any N=3 block. (session-settled: user-directed — chosen over `<expand to all 5–7 categories>`: budget math — tier-0 (5) + tier-4 (4) = 9 = the cap.)

### Requirements

**Live-data amplification (R1–R5).**

- **R1.** Step 3.5 in `references/agents/meta-top-digital-researcher.md` MUST raise the tier-4 cap to 4 when N=3 (all top-3 categories lack `observed_live` after tier-3). When N=3 fires tier-4, the data-quality note records `tier-4 cap raised: 2 → 4 (N=3 full-block fallback)`.
- **R2.** Tier-0 in `SKILL.md` and the researcher MUST cover the top-5 `digital_categories` from `references/regions/<region>.yaml` (was top-3). Total Playwright nav budget per invocation stays ≤9.
- **R3.** A new `scripts/lib/cache.py` provides a 24-hour disk cache keyed by `(tier, query_hash, region)`. Cache stores ONLY tier-1 and tier-2 search-result payloads (list of `{url, title, snippet}` dicts); it MUST reject any write whose payload contains a `pricing_examples`, `underground_signals`, `winning_score`, `tier_used == "playwright"`, or any other pricing/inventory field. Document the rejection logic with inline comments citing R3.
- **R4.** `scripts/lib/web_search_keyless.py` MUST cycle through 3–5 public SearXNG instances when the configured `META_TOP_SEARXNG_URL` returns 0 results or fails. Each instance is tried with the same exponential backoff already in `_request()`. After all instances fail, the function falls through to DuckDuckGo HTML as before. The instance list is a module-level constant `PUBLIC_SEARXNG_INSTANCES` with a short comment explaining how the list is maintained (hand-curated; community-maintained mirrors break regularly).
- **R5.** The researcher MUST dispatch tier-1 (WebSearch), tier-2 (keyless), and tier-3 (WebFetch) in parallel via `Agent` tool fan-out where the host allows. Tier-0 (Playwright) and tier-4 (Playwright fallback) stay serial because both are budget-bound to a single browser context. Document the parallel/serial split with an inline comment citing R5.

**Fail-closed preservation (R6–R8).**

- **R6.** The v1.5 hard-block callout (`category-pricing-research-required`) MUST still appear when, after all five rungs (tier-0, tier-1, tier-2, tier-3, tier-4) fire, 0 of 3 top categories carry `pricing_examples[].pricing_tier_source: observed_live`. The cap-raise note is appended to `data_quality_note` ONLY when tier-4 fired.
- **R7.** The cache layer MUST NOT mutate any field covered by the v1.5 `pricing_tier_source` enum. The `observed_live` provenance (with its `accessed_at`, `tier_used`, `kind`, citation URL) MUST be regenerated on every brief invocation, never reused from cache.
- **R8.** The hard-block threshold (≤1 of 3 → brief ships with caveats; 0 of 3 → block) is unchanged from v1.5. Step 3.5 only changes WHICH categories trigger the cap raise, not the threshold semantics.

**Mirror parity (R9).**

- **R9.** `skills/meta-top/` MUST receive the R3 (`cache.py`), R4 (`web_search_keyless.py`), and R5 (`researcher.md`) changes on the same files. SKILL.md at `skills/meta-top/` gets a parallel source-ladder description update (multi-instance SearXNG, cache, parallel dispatch) and a v1.6 version-history bump — but does NOT mirror U1's Step 3.5 logic revision or U2's tier-0 expansion (meta-top has different ladder semantics: tier-0 already mandatory per category; no tier-4 Playwright fallback to revise). The byte-identity check (U6 verification) covers `cache.py` and `web_search_keyless.py` only; `http.py` is unchanged in this revision and inherits prior parity.

### Success Criteria

- **SC1.** A simulated IN run where tier-1 returns 0 (rate-limited) AND tier-3 returns 403/404 on ≥4 URLs clears the hard-block via tier-4 Playwright in the v1.7 cap-raised scenario (R1, N=3 now fires tier-4 alongside N=1/N=2), instead of short-circuiting as it did in v1.6.
- **SC2.** A repeated IN run within 24 hours on the same region sees the tier-1 WebSearch call hit the disk cache (R3) and complete in <2 seconds, vs. ~15–30 seconds for a fresh WebSearch.
- **SC3.** A tier-2 keyless-search invocation against a stale `META_TOP_SEARXNG_URL` cycles through ≥2 backup instances (R4) before reporting the rate-limited state, vs. failing on the first instance as in v1.6.
- **SC4.** A parallel-dispatched researcher run completes in ≤70% of the v1.6 wall-clock for the same input (R5).
- **SC5.** The v1.5 hard-block callout still fires when tier-0 + tier-1 + tier-2 + tier-3 + tier-4 all fail to produce `observed_live` for any of the 3 top categories (R6).

### Scope Boundaries

**In scope.** Six changes: R1 Step 3.5 revision, R2 tier-0 expansion, R3 cache layer, R4 multi-instance SearXNG, R5 parallel tier firing, R9 mirror parity.

**Out of scope (carrying forward).**
- Wayback Machine fallback — pricing staleness defeats the skill's purpose (KD1).
- Tier-3 marketplace snapshot cache — same reason (KD1).
- v1.5 hard-block threshold change — fail-closed semantics preserved (R6, R7, R8).
- Pricing/inventory caching — pricing changes weekly or faster (KD2, R3, R7).
- New external services — no ScrapeCreators, no Apify, no paid APIs (KD1, KD2).
- A scraper for Instagram comment depth — out of scope, no API hooks.

### Risks & Dependencies

- **Risk: Public SearXNG instances break.** Community mirrors go down regularly; a hand-curated list will go stale. **Mitigation:** the `PUBLIC_SEARXNG_INSTANCES` constant carries a docstring on how to refresh (check https://searx.space for live instances, prefer https over http, prefer non-CAPTCHA instances). Each broken instance logs a one-line warning; the rung does not fail just because one mirror is down.
- **Risk: Disk cache grows unbounded.** With dozens of queries per day across multiple regions, the cache dir could balloon. **Mitigation:** the cache layer enforces a 1 GB cap with LRU eviction; an additional `META_TOP_CACHE_MAX_BYTES` env var lets the user tune the cap.
- **Risk: Parallel dispatch amplifies rate-limit hits.** If tier-1 and tier-2 fire simultaneously, the rate limiter may double-deny. **Mitigation:** the researcher staggers tier-1 and tier-2 by a 500ms jitter (`random.uniform(0, 0.5)`) before dispatch; this stays well under the rate-limit window but spreads the burst.
- **Risk: Mirror parity drift.** `skills/meta-top/` and `skills/meta-top-digital/` diverge over time as features land in one but not the other. **Mitigation:** R9 mandates mirror sync; a unit-level checklist enforces it.

## Planning Contract

### Key Technical Decisions

- **KTD1. Cache scope is search-results-only.** R3. Cache key: `(tier, query_hash, region)` where `tier ∈ {"tier1_websearch", "tier2_keyless"}`. `query_hash` is `sha256(query.encode('utf-8')).hexdigest()[:16]` (first 16 hex chars; collision probability ~1e-19 for ≤1000 distinct queries). The tuple is itself hashed with `sha256(f'{tier}|{query_hash}|{region}'.encode('utf-8')).hexdigest()` to form the cache filename, preventing collision-based overwrites between tiers and regions. Cache value: list of `{url, title, snippet}` dicts. Reject writes that include `pricing_examples`, `underground_signals`, `winning_score`, `accessed_at`, `tier_used` (when tier is playwright), `currency`, or `kind` field. Rejection logs a one-line warning to stderr with the field name. Implementation: a `safe_cache_get(key: str) → list[dict] | None` and `safe_cache_put(key: str, payload: list[dict]) → bool` pair that filters payloads before write.
- **KTD2. Real-time pricing via Playwright.** R1, R2. Every `pricing_examples[].pricing_tier_source: observed_live` entry MUST be regenerated on every brief invocation; the `accessed_at` timestamp MUST be within the same UTC day as the brief's `snapshot_date`. The cache layer is forbidden from storing or returning observed_live entries.
- **KTD3. Hand-curated SearXNG instance list.** R4. A module-level `PUBLIC_SEARXNG_INSTANCES: list[str]` carries 5 community-maintained instances as a starting point. The list is documented as "refresh quarterly from https://searx.space; community mirrors rotate regularly." When the configured `META_TOP_SEARXNG_URL` is unset, the rung cycles through the public list. When set, the rung tries the configured URL first, then falls through to the public list on 0-result or error.
- **KTD4. Parallel dispatch with Playwright serial.** R5. Tier-1 (WebSearch), tier-2 (keyless), tier-3 (WebFetch) fire in parallel via `Agent` tool fan-out. Tier-0 (Meta Ad Library Playwright) and tier-4 (Playwright fallback) stay serial within a single browser context — they share the ≤9 nav budget and cannot safely share context with non-Playwright tiers. Document the split inline.
- **KTD5. Mirror parity enforcement.** R9. The shared modules (`scripts/lib/cache.py`, `scripts/lib/web_search_keyless.py`, `scripts/lib/http.py`) live under `scripts/lib/` in both skills. They MUST be byte-identical at commit time. The mirror sync unit (U6) verifies byte-identity via `git diff` between the two paths before commit.

### High-Level Technical Design

Six independent edits across two skills, plus a new shared module:

```
skills/meta-top-digital/                          skills/meta-top/
├── SKILL.md                          [edit]      ├── SKILL.md                          [edit, source ladder description only]
├── references/
│   ├── agents/
│   │   └── meta-top-digital-researcher.md        │   ├── agents/
│   │                                [edit]      │   │   └── meta-top-researcher.md     [edit, R5 parallel only]
│   └── regions/
│       └── in.yaml                                │   └── regions/
├── scripts/
│   ├── keyless_search.py             [edit]      ├── scripts/
│   └── lib/                                      │   └── lib/
│       ├── cache.py                  [new]        │       ├── cache.py                  [new, byte-identical mirror]
│       ├── http.py                   [unchanged, parity preserved]      │       ├── http.py                   [unchanged, parity preserved]
│       └── web_search_keyless.py     [edit]       │       └── web_search_keyless.py     [edit, mirror]
```

The new `cache.py` is the only new file. All other changes are edits.

### Sequencing

The six units can ship in any order, but the cleanest order is:

1. **U3 (cache.py)** — independent, new file; unblocks downstream edits.
2. **U4 (multi-instance SearXNG)** — depends on `http.py` (already shared).
3. **U5 (parallel tier firing)** — touches researcher.md only.
4. **U1 (Step 3.5 logic)** — touches researcher.md; benefits from running U5 first so both edits land together.
5. **U2 (tier-0 expansion)** — touches researcher.md + SKILL.md.
6. **U6 (mirror sync)** — last; runs after all five digital-only edits to confirm parity on shared modules.

## Implementation Units

### U1. Step 3.5 logic revision (meta-top-digital only)

**Goal.** When all 3 top categories lack `observed_live` after tier-3, tier-4 fires with cap=4 to attempt clearing the hard-block via Playwright.

**Requirements.** R1, R6, R7, R8.

**Files.**
- `C:\Users\HP\.claude\skills\meta-top-digital\references\agents\meta-top-digital-researcher.md` (lines 162–186, the Step 3.5 cap-raise gate)
- `C:\Users\HP\.claude\skills\meta-top-digital\SKILL.md` (the `Reliability: source ladder > 4. Playwright browser fallback` paragraph, where the v1.6 N=3 cap-does-not-raise wording contradicts the new R1 behavior)

**Approach.**
Replace the v1.6 N=3 branch ("do not fire tier-4") with a fire-with-cap-4 branch. Preserve the v1.6 N=1/N=2 and N=0 branches verbatim. Append a one-line `data_quality_note` recording the cap raise. Add an inline comment citing R1 and KD3 so the next editor sees the rationale.

Pseudocode after the edit:
```python
top3 = top_categories.slice(0, 3)
def has_observed_live(c):
    ex = c.get("pricing_examples", [])
    return len(ex) > 0 and any(p.get("pricing_tier_source") == "observed_live" for p in ex)
lacking = [c for c in top3 if not has_observed_live(c)]
N = len(lacking)

# v1.7+ (R1, KD3): all three branches fire tier-4 — fail-closed is preserved by
# the v1.5 hard-block callout, which still fires if tier-4 also fails to produce
# observed_live. The change is only the path TO the block, not the block itself.
if N == 0:
    tier_4_cap = 2
elif N == 1 or N == 2:
    tier_4_cap = 4
    append_to_data_quality_note(f"tier-4 cap raised: 2 → 4 ({N} of 3 categories still lack observed_live)")
else:  # N == 3
    tier_4_cap = 4
    append_to_data_quality_note("tier-4 cap raised: 2 → 4 (N=3 full-block fallback; hard-block fires if tier-4 also fails)")
```

**Test scenarios.**
- N=0 → cap=2, no note.
- N=1 → cap=4, note records 1/3.
- N=2 → cap=4, note records 2/3.
- N=3 → cap=4, note records N=3 full-block fallback (NEW behavior).

**Verification.** `python -c "import re; src = open(r'C:\Users\HP\.claude\skills\meta-top-digital\references\agents\meta-top-digital-researcher.md', encoding='utf-8').read(); assert 'N == 3' in src and 'tier_4_cap = 4' in src"`.

### U2. Tier-0 expansion to top-5 (meta-top-digital only)

**Goal.** Tier-0 covers the top-5 categories from the region YAML, expanding from top-3.

**Requirements.** R2, R8.

**Files.**
- `C:\Users\HP\.claude\skills\meta-top-digital\SKILL.md` (lines 88–95, tier-0 description; bump version `v1.6 → v1.7` and add the v1.7 line to the version-history block)
- `C:\Users\HP\.claude\skills\meta-top-digital\references\agents\meta-top-digital-researcher.md` (the Step 3.0.0 tier-0 navigation list, change `top-3` → `top-5`)

**Approach.**
Bump the SKILL.md version from v1.6 to v1.7 in the badge line and the SKILL CONTRACT version block. Add a v1.7 line: `v1.7 (2026-09-29) adds Step 3.5 N=3 fire-with-cap-4 path, expands tier-0 from top-3 to top-5, adds 24h disk cache for tier-1/tier-2 search results only, multi-instance SearXNG fallback, and parallel tier-1/tier-2/tier-3 dispatch. v1.6 winning-verdict callout and v1.5 hard-block unchanged.`

Change the cap-budget line in SKILL.md: `Cap: ≤5 Playwright navigations per invocation` stays correct (was 3 navs for top-3 in v1.6; top-5 in v1.7 still ≤5 since tier-0 keeps one nav per category, so the total stays ≤5). The total budget line stays `Total Playwright nav budget ≤9 per invocation (≤5 tier-0 + ≤4 tier-4)`.

In the researcher.md, change `for EACH top-3 category` to `for EACH top-5 category` in the Step 3.0.0 description. The prior `Total Playwright nav budget ≤7 per invocation (≤5 tier-0 + ≤2 tier-4)` line in the source-ladder summary is updated to `≤9 per invocation (≤5 tier-0 + ≤4 tier-4)` to reflect the v1.6 conditional cap raise AND the v1.7 N=3 always-fire path. Add inline comments citing R2 and KD5.

**Test scenarios.**
- SKILL.md version reads `v1.7` and the v1.7 line appears.
- researcher.md says top-5.
- Cap budgets (≤5 tier-0, ≤4 tier-4, ≤9 total) are unchanged.

**Verification.** `grep -n "top-5\|top-3" references/agents/meta-top-digital-researcher.md | head -20` — confirm only `top-5` remains in the tier-0 context.

### U3. 24-hour disk cache for tier-1/tier-2 search results

**Goal.** New `scripts/lib/cache.py` provides a 24-hour disk cache keyed by `(tier, query_hash, region)` that stores ONLY search-result payloads. Mirror the file to both skills.

**Requirements.** R3, R7, R9.

**Files.**
- `C:\Users\HP\.claude\skills\meta-top-digital\scripts\lib\cache.py` (NEW)
- `C:\Users\HP\.claude\skills\meta-top\scripts\lib\cache.py` (NEW, byte-identical mirror)

**Approach.**
- Use stdlib-only: `hashlib`, `json`, `os`, `time`, `pathlib`. No external deps.
- Cache dir: `$TMPDIR/meta-top-cache/v1/` (or `%TEMP%\meta-top-cache\v1` on Windows; fall back to `~/.cache/meta-top/v1/`). Overridable via `META_TOP_CACHE_DIR` env var when `$TMPDIR` is read-only.
- Cache file naming: `<sha256(f'{tier}|{query_hash}|{region}')>.json` where `query_hash = sha256(query.encode('utf-8')).hexdigest()[:16]` (16-hex-char truncation; collision probability ~1e-19 for ≤1000 distinct queries). Same hash spec as KTD1.
- TTL: 86_400 seconds (24 hours).
- LRU eviction: cap at 1 GB by default; tunable via `META_TOP_CACHE_MAX_BYTES` env var. Algorithm: on `safe_cache_put`, compute current dir size; if it exceeds the cap, walk the dir sorted by `mtime` ascending and unlink the oldest files until size is at or below the cap. This is an O(n) mtime scan per eviction event — acceptable because cache writes happen at most ~50/invocation and the dir typically holds ~1000 files after weeks of use.
- Public API:
  - `safe_cache_get(key: str) -> list[dict] | None` — returns the cached payload or None.
  - `safe_cache_put(key: str, payload: list[dict]) -> bool` — returns True on success, False on rejection.
- Rejection rules (R3, R7): `safe_cache_put` rejects payloads containing any of these field names at any depth: `pricing_examples`, `underground_signals`, `winning_score`, `accessed_at`, `tier_used` (when tier is playwright), `currency`, `kind`. Rejection logs `[cache] refused: payload contains <field>` to stderr. Same field set as KTD1.
- `scripts/lib/web_search_keyless.py` (the lib path used by both skills; the legacy `scripts/keyless_search.py` is the deprecated v1.3 shim and is NOT modified) is updated to call `safe_cache_get` before each query and `safe_cache_put` after each successful result.

**Test scenarios.**
- `safe_cache_put(["http://example.com", "Snippet text"], [{pricing_examples: [...]}])` returns False and logs the rejection.
- `safe_cache_put("foo", [{"url": "...", "title": "...", "snippet": "..."}])` returns True.
- Second call to `safe_cache_get("foo")` within 24h returns the cached value.
- After 24h, `safe_cache_get("foo")` returns None.

**Verification.** `python -c "import sys; sys.path.insert(0, r'C:\Users\HP\.claude\skills\meta-top-digital\scripts\lib'); from cache import safe_cache_get, safe_cache_put; assert safe_cache_put('t1:foo:in', [{'url': 'x', 'title': 't', 'snippet': 's'}]); assert safe_cache_get('t1:foo:in') == [{'url': 'x', 'title': 't', 'snippet': 's'}]"`.

### U4. Multi-instance SearXNG fallback

**Goal.** When the configured `META_TOP_SEARXNG_URL` returns 0 results or fails, cycle through 3–5 public SearXNG instances.

**Requirements.** R4.

**Files.**
- `C:\Users\HP\.claude\skills\meta-top-digital\scripts\lib\web_search_keyless.py`
- `C:\Users\HP\.claude\skills\meta-top\scripts\lib\web_search_keyless.py` (byte-identical mirror)

**Approach.**
Add `PUBLIC_SEARXNG_INSTANCES: list[str]` at module top with 5 community-maintained instances as a starting point. Each instance is tried with the existing exponential-backoff `_request()`. The function tries them in order, returns the first non-empty result set, and falls through to DuckDuckGo HTML only when all 5 fail.

Pseudocode sketch (the file is small; this is the entry-point shape):
```python
PUBLIC_SEARXNG_INSTANCES = [
    "https://searx.be",
    "https://search.sapti.me",
    "https://searx.tiekoetter.com",
    "https://searxng.nicfab.eu",
    "https://baresearch.org",
]

def searxng_search(query: str, count: int, instance_url: str) -> list[dict]:
    # existing single-instance logic, parameterized on instance_url
    ...

def keyless_search(
    query: str,
    count: int = 5,
    *,
    searxng_url: str | None = None,
) -> tuple[list[dict], str | None]:
    """Returns (results, instance_url_used).
    Preserves the v1.6 tuple signature so existing callers/tests don't break.
    `searxng_url` keyword overrides `META_TOP_SEARXNG_URL` env var (used by tests).
    Returns ([], None) only after both SearXNG cycle AND DDG HTML fallback fail.
    """
    configured = (
        searxng_url
        if searxng_url is not None
        else os.environ.get("META_TOP_SEARXNG_URL", "")
    )
    instances = [configured] + [u for u in PUBLIC_SEARXNG_INSTANCES if u]
    for inst in instances:
        results = searxng_search(query, count, inst)
        if results:
            return results, inst
    # fall through to DDG HTML as before
    return ddg_html_search(query, count), None
```

Add an inline comment on `PUBLIC_SEARXNG_INSTANCES` noting that community mirrors rotate regularly; refresh quarterly from https://searx.space.

**Test scenarios.**
- `META_TOP_SEARXNG_URL=""` and DDG returns 0 → function tries ≥2 public SearXNG instances before returning `[]`.
- One instance fails (raises) → loop continues to next instance.
- All instances return 0 → function falls through to DDG HTML.

**Verification.** `python -c "import sys; sys.path.insert(0, r'C:\Users\HP\.claude\skills\meta-top-digital\scripts\lib'); from web_search_keyless import PUBLIC_SEARXNG_INSTANCES; assert len(PUBLIC_SEARXNG_INSTANCES) >= 3"`.

### U5. Parallel tier-1/tier-2/tier-3 dispatch

**Goal.** The researcher dispatches tier-1, tier-2, and tier-3 in parallel where the host allows.

**Requirements.** R5.

**Files.**
- `C:\Users\HP\.claude\skills\meta-top-digital\references\agents\meta-top-digital-researcher.md` (the Step 3 ladder dispatch section)
- `C:\Users\HP\.claude\skills\meta-top\references\agents\meta-top-researcher.md` (mirror, R9)

**Approach.**
- Tier-1 (WebSearch), tier-2 (keyless_search.py via Bash), tier-3 (WebFetch curated marketplaces) fire in parallel via `Agent` tool fan-out OR via concurrent `Bash`/`WebSearch`/`WebFetch` calls in the same tool block. The exact dispatch shape depends on the host's parallel-allowed tool list; the researcher picks the cheapest shape.
- Tier-0 and tier-4 stay serial — both are Playwright and share the ≤9 nav budget.
- Add a 500ms `random.uniform(0, 0.5)` jitter before tier-1 and tier-2 fire to spread the burst (per the Risks section).
- Inline comment citing R5 and KTD4 documents the split.

**Test scenarios.**
- Researcher output: tier-1 and tier-2 start timestamps are within 600ms of each other (the jitter window).
- Tier-0 fires only after tier-1/tier-2/tier-3 return.
- Tier-4 fires only after tier-0/tier-1/tier-2/tier-3 return AND Step 3.5 raises the cap.

**Verification.** Manual: read the dispatch section and confirm the parallel calls are documented.

### U6. Mirror sync to `skills/meta-top/`

**Goal.** The shared modules land at `skills/meta-top/` byte-identical to `skills/meta-top-digital/`.

**Requirements.** R9.

**Files.**
- `C:\Users\HP\.claude\skills\meta-top\scripts\lib\cache.py` (NEW)
- `C:\Users\HP\.claude\skills\meta-top\scripts\lib\web_search_keyless.py` (edit)
- `C:\Users\HP\.claude\skills\meta-top\scripts\lib\http.py` (edit, if http.py changes; in this revision, http.py is unchanged, only listed for tracking)
- `C:\Users\HP\.claude\skills\meta-top\references\agents\meta-top-researcher.md` (edit, R5 parallel only)
- `C:\Users\HP\.claude\skills\meta-top\SKILL.md` (edit, source-ladder description; bump to v1.6 (single minor bump from v1.5; meta-top's tier-0/tier-4 ladder differs so it does not need a v1.7 bump). Add the v1.6 line: `v1.6 (2026-09-29) adds multi-instance SearXNG fallback, 24h disk cache for search results, and parallel tier-1/tier-2/tier-3 dispatch (mirror of meta-top-digital v1.7 infra). v1.5 hard-block and source ladder tiers unchanged.`)

**Approach.**
- For `cache.py`: copy U3's file verbatim.
- For `web_search_keyless.py`: copy U4's edits verbatim (byte-identical).
- For `http.py`: unchanged in this revision.
- For `meta-top-researcher.md`: apply U5's parallel-tier dispatch edits; do NOT mirror U1 (Step 3.5) or U2 (tier-0 expansion) — meta-top has different ladder semantics (tier-0 already mandatory per category; no tier-4 Playwright fallback).
- For `meta-top SKILL.md`: update the source-ladder description to mention multi-instance SearXNG, the cache, and parallel dispatch. Add the appropriate version-history line.

**Verification.**
```bash
# Confirm shared modules are byte-identical
diff -q "C:/Users/HP/.claude/skills/meta-top-digital/scripts/lib/cache.py" \
        "C:/Users/HP/.claude/skills/meta-top/scripts/lib/cache.py"
diff -q "C:/Users/HP/.claude/skills/meta-top-digital/scripts/lib/web_search_keyless.py" \
        "C:/Users/HP/.claude/skills/meta-top/scripts/lib/web_search_keyless.py"
# Expected: no output (identical files)
```

## Verification Contract

**Repo-specific commands.**

The meta-top repo has no automated test suite for the skills. Verification is a manual smoke test:

0. **Baseline capture (SC4):** Run `/meta-top-digital in` once against v1.6 (no v1.7 infra) and record the wall-clock from invocation start to output. The v1.7 target is ≤70% of this baseline. Capture the value into the PR description for review; the smoke test below validates against it.
1. **U1 / U2 (researcher.md and SKILL.md edits):** Read the diff. Confirm the Step 3.5 N=3 branch fires tier-4 with cap=4 and the data_quality_note records it. Confirm the tier-0 cap description reads top-5.
2. **U3 (cache.py):** Run the inline verification Python snippet above. Run a second invocation of the same query within 24h and confirm the cache hit (look for `[cache] hit: <key>` log line in stderr).
3. **U4 (multi-instance SearXNG):** Run `python -c "import sys; sys.path.insert(0, r'C:\Users\HP\.claude\skills\meta-top-digital\scripts\lib'); from web_search_keyless import PUBLIC_SEARXNG_INSTANCES; print(len(PUBLIC_SEARXNG_INSTANCES))"`. Expected output: `5`.
4. **U5 (parallel dispatch):** Read the dispatch section in researcher.md. Confirm the parallel calls and the serial tier-0/tier-4 split are documented.
5. **U6 (mirror parity):** Run the diff snippet above. Expected: no output.
6. **Smoke test (R1 SC1):** Run `/meta-top-digital in` and confirm the brief ships with observed_live pricing for ≥1 category (or the hard-block callout fires cleanly with the new `tier-4 cap raised: 2 → 4 (N=3 full-block fallback)` note).

**Quality gates.**
- All edits stay within the unit's `Files:` list (scope discipline).
- No new external dependencies; stdlib-only for the Python additions.
- Mirror paths under `C:\Users\HP\.claude\skills\` are edited first; the working copy at `C:\Users\HP\projects\meta-top\skills\` is the mirror.
- No Claude Code footer in any commit message or PR description.

## Definition of Done

**Global.**
- All six units ship in one PR (or six linked commits) on the meta-top working branch.
- The mirror at `C:\Users\HP\projects\meta-top\skills\` is updated to match the live skills.
- A smoke-test run of `/meta-top-digital in` completes within ≤70% of v1.6 wall-clock for the same input.
- The v1.5 hard-block callout still fires when tier-0 through tier-4 all fail to produce `observed_live`.
- The meta-top-digital SKILL.md carries the v1.7 version-history line; the meta-top SKILL.md carries the v1.6 line (single minor bump from v1.5; meta-top's tier-0/tier-4 ladder differs so it does not need a v1.7 bump). Each skill's version line reflects its own version.

**Per-unit.**
- U1: Step 3.5 N=3 branch fires tier-4 with cap=4; verification Python snippet returns clean.
- U2: Tier-0 covers top-5; SKILL.md reads v1.7 with the new version-history line.
- U3: `cache.py` exists at both skills; round-trip test passes; pricing payloads are rejected.
- U4: `PUBLIC_SEARXNG_INSTANCES` has ≥3 entries; inline verification returns `5`.
- U5: Researcher dispatch section documents parallel tier-1/tier-2/tier-3 and serial tier-0/tier-4.
- U6: `diff` between the two `cache.py` files and the two `web_search_keyless.py` files produces no output.

**Cleanup.** No abandoned-attempt code. The N=3 branch's `tier-4 cap raised: 2 → 4 (N=3 full-block fallback; hard-block fires if tier-4 also fails)` data_quality_note is the new v1.7 wording in U1; the N=1/N=2 wording `tier-4 cap raised: 2 → 4 (N of 3 categories still lack observed_live)` carries forward from v1.6 unchanged. No stale branches remain.

## Appendix

### Sources / Research

- **v1.5 hard-block semantics (R6, R7, R8).** `C:\Users\HP\.claude\skills\meta-top-digital\SKILL.md` lines 75–110, the Hard-Block section. Fail-closed contract is preserved verbatim; this revision only changes the path TO the block.
- **v1.6 Step 3.5 logic (R1).** `C:\Users\HP\.claude\skills\meta-top-digital\references\agents\meta-top-digital-researcher.md` lines 162–186, the Step 3.5 cap-raise gate. The N=3 branch is the only line changed.
- **v1.6 tier-0 cap (R2).** `C:\Users\HP\.claude\skills\meta-top-digital\SKILL.md` lines 88–95, the tier-0 description. Cap budget math: tier-0 (5) + tier-4 (4) = 9 = the cap.
- **keyless_search.py entry point (R3, R4).** `C:\Users\HP\.claude\skills\meta-top-digital\scripts\keyless_search.py` and `C:\Users\HP\.claude\skills\meta-top-digital\scripts\lib\web_search_keyless.py`. Stdlib-only; no new deps.
- **memory: `meta-top-digital full research default`.** The memory entry prescribes firing tier-4 on a broader signal set (`partial_research: true`, `rate_limit_hit: true`, any inferred pricing tier, any `confidence:low` signal). This plan keeps the narrower N-based trigger (R1) and treats the broader memory rule as **out of scope for this revision** — future iterations may widen R1 to fire on the memory's full signal set; v1.7 only commits to firing on N≥1 of top-3 lacking `observed_live`.
- **No `<root>/solutions/` directory.** `C:\Users\HP\projects\meta-top\` has no `solutions/` subdirectory, so no existing learnings to mine. The v1.5 hard-block learning lives in the SKILL.md text, not in a separate file.

### Open Questions

None. The five user-confirmed decisions cover the surface area. KD1 (no Wayback Machine) and KD2 (cache scope) were settled by the user during synthesis.

### Deferred questions (from ce-doc-review)

- **Q1. Playwright as escape valve (P0, product-lens).** The product-lens reviewer argued that relying on Playwright to clear rate-limit-induced blocks makes the skill fragile — if Playwright itself rate-limits (Meta Ad Library verification wall, marketplace anti-bot), the skill still collapses. The user's AskUserQuestion answer ("fire tier-4 with cap=4 in N=3") settled this in favor of amplifying Playwright; the v1.7 design treats Playwright as a load-bearing tier, not a backup. **Resolved by KD3 + R1**; carried forward for awareness.
- **Q2. Cache value vs. complexity (P2, product-lens).** The product-lens reviewer noted the cache adds a module, an LRU eviction pass, and a config var for marginal gain on a single-region-day-after-day workflow. The user-confirmed scope (KD2) keeps the cache for the second-day repeat case (SC2: <2s vs ~15–30s); the module stays small (~100 lines, stdlib-only). **Resolved by KD2 + U3**; carry-forward only if v1.8 evaluation shows <5% repeat-invocation rate.
- **Q3. Pre-synthesis open question: commit v1.4 and v1.5 plan files?** Plans `2026-09-28-meta-ads-library-tier0-v14.md` and `2026-09-29-meta-top-digital-v15-improvements.md` exist as working-copy files; user has not authorized commit. Surface this for the post-implementation phase.

### Pre-synthesis reference

The original proposed synthesis included Wayback Machine fallback, tier-3 marketplace snapshot cache, and a 24-hour cache for pricing/inventory. All three were dropped after user pushback ("I want realtime research done to gather data to find the winning product. disk cache, wayback machine, etc will make the research outdated. wont it?"). The revised synthesis is what's written above.
