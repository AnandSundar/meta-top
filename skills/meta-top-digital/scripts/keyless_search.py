#!/usr/bin/env python3
"""CLI entry point for meta-top's keyless search floor.

The meta-top sub-agent invokes this via Bash after WebSearch returns 0 sources:

    python <skill-root>/scripts/keyless_search.py "QUERY" --count 5

Reads ``META_TOP_SEARXNG_URL`` from env to enable the SearXNG fallback rung
(also overridable via ``--searxng-url``). Outputs JSON to stdout matching the
shape consumed by the orchestrator. Exit codes:

  0 — at least one result returned.
  2 — zero results (caller should walk the source ladder to tier 3).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

# ``scripts/keyless_search.py`` lives one level above ``lib/``; adding the
# script's directory to sys.path makes ``from lib ...`` resolvable regardless
# of the caller's cwd.
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from lib.web_search_keyless import keyless_search  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="meta-top keyless search floor (DDG HTML + optional SearXNG)"
    )
    parser.add_argument("query", help="Search query")
    parser.add_argument(
        "--count",
        type=int,
        default=5,
        help="Maximum number of results to return (default: 5)",
    )
    parser.add_argument(
        "--searxng-url",
        default=os.environ.get("META_TOP_SEARXNG_URL", ""),
        help=(
            "Optional SearXNG instance URL used as a fallback when DuckDuckGo "
            "returns 0 results. Also reads META_TOP_SEARXNG_URL env var."
        ),
    )
    args = parser.parse_args()
    items, artifact = keyless_search(
        args.query, count=args.count, searxng_url=args.searxng_url
    )
    print(json.dumps({"results": items, "artifact": artifact}, indent=2))
    if not items:
        return 2  # surface non-zero so the sub-agent sees the empty-result signal
    return 0


if __name__ == "__main__":
    sys.exit(main())
