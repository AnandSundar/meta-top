# F16 Baseline Log — meta-top-digital

Per-invocation log appended by `meta-top-digital-researcher.md` Step 3.5 (v1.9, R5). Schema: `<ISO8601> <region> <observed_live_lacking:0-3> <partial_research:0|1> <rate_limit_hit:0|1> <verification_wall_hit:0|1> <inferred_seed:0|1> <outcome:succeeded|partial|blocked> <latency_ms:integer>`.

For empirical validation of latency-budget raise (Q5). v1.9.1+ calibration work consults this log; v1.9 ships no behavior that gates on it.

<!-- Log entries append below this line. Format: <ISO8601> <region> <observed_live_lacking> <partial_research> <rate_limit_hit> <verification_wall_hit> <inferred_seed> <outcome> <latency_ms> -->