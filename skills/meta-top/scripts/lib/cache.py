"""Search-result disk cache for meta-top and meta-top-digital.

Per the v1.7 plan (R3, KTD1, R9). Stores ONLY tier-1 (WebSearch) and tier-2
(keyless DDG/SearXNG) search-result payloads -- list of {url, title, snippet}
dicts. NEVER stores pricing, inventory, winning scores, or any other
load-bearing brief field.

Rejection is enforced at write time: payloads containing any of the protected
field names (`pricing_examples`, `underground_signals`, `winning_score`,
`accessed_at`, `tier_used`, `currency`, `kind`) are refused with a stderr
warning. This is the only line of defense against the cache leaking
observed-live data -- read-side checks are intentionally absent so a
corrupted cache file cannot be served (it would never be written in the
first place).

Key shape: `<tier>:<query_hash>:<region>` where `query_hash` is
`sha256(query.encode('utf-8')).hexdigest()[:16]` (16-hex-char truncation;
collision probability ~1e-19 for <=1000 distinct queries). The composite key
is itself hashed with sha256 to form the on-disk filename, preventing
collision-based overwrites between tiers and regions.

Cache dir: $TMPDIR/meta-top-cache/v1/ (or %TEMP%\\meta-top-cache\\v1 on
Windows; falls back to ~/.cache/meta-top/v1/). Override via META_TOP_CACHE_DIR.
TTL: 86_400 seconds (24 hours). LRU eviction cap: 1 GB default; tunable via
META_TOP_CACHE_MAX_BYTES. Algorithm: on safe_cache_put, compute current dir
size; if over the cap, unlink oldest-mtime files until at or below cap.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

# v1.7 plan R3, KTD1: rejection field set (union of plan fields cited by
# coherence + feasibility reviewers). The cache never serves any of these.
REJECTED_FIELDS = frozenset({
    "pricing_examples",
    "underground_signals",
    "winning_score",
    "accessed_at",
    "tier_used",  # observed-live tier (playwright) is provenance; rejected here
    "currency",
    "kind",
})

DEFAULT_TTL_SECONDS = 86_400  # 24 hours
DEFAULT_MAX_BYTES = 1 * 1024 * 1024 * 1024  # 1 GB
CACHE_SUBDIR = "meta-top-cache/v1"


def _cache_dir() -> Path:
    """Resolve the cache directory in priority order:
    1. META_TOP_CACHE_DIR env var (if set and writable)
    2. $TMPDIR/meta-top-cache/v1/ (POSIX) or %TEMP%\\meta-top-cache\\v1 (Windows)
    3. ~/.cache/meta-top/v1/ (user-home fallback)
    """
    override = os.environ.get("META_TOP_CACHE_DIR")
    if override:
        p = Path(override)
        try:
            p.mkdir(parents=True, exist_ok=True)
            return p
        except OSError:
            pass  # fall through to defaults

    tmp = os.environ.get("TMPDIR") or tempfile.gettempdir()
    p = Path(tmp) / CACHE_SUBDIR
    try:
        p.mkdir(parents=True, exist_ok=True)
        # Verify writability with a tiny probe file.
        probe = p / ".write_probe"
        probe.write_text("ok")
        probe.unlink()
        return p
    except OSError:
        home = Path.home() / ".cache" / "meta-top" / "v1"
        home.mkdir(parents=True, exist_ok=True)
        return home


def _filename_for(key: str) -> Path:
    """sha256 the composite key to form the on-disk filename."""
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return _cache_dir() / f"{digest}.json"


def _has_rejected_field(payload: Any) -> str | None:
    """Walk the payload recursively; return the first rejected field name found.

    A "field name" is a dict key whose name matches one of REJECTED_FIELDS.
    Values can be anything -- the mere presence of the key rejects the write.
    """
    stack: list[Any] = [payload]
    while stack:
        node = stack.pop()
        if isinstance(node, dict):
            for k, v in node.items():
                if k in REJECTED_FIELDS:
                    return k
                stack.append(v)
        elif isinstance(node, list):
            stack.extend(node)
    return None


def _dir_size_bytes(dir_path: Path) -> int:
    total = 0
    for child in dir_path.iterdir():
        try:
            if child.is_file():
                total += child.stat().st_size
            elif child.is_dir():
                total += _dir_size_bytes(child)
        except OSError:
            continue
    return total


def _evict_to_cap(dir_path: Path, cap_bytes: int) -> None:
    """LRU eviction: unlink oldest-mtime files until size <= cap."""
    if cap_bytes <= 0:
        return
    while _dir_size_bytes(dir_path) > cap_bytes:
        try:
            candidates = sorted(
                (p for p in dir_path.iterdir() if p.is_file() and p.suffix == ".json"),
                key=lambda p: p.stat().st_mtime,
            )
        except OSError:
            return
        if not candidates:
            return
        try:
            candidates[0].unlink()
        except OSError:
            # Unlinkable file (permissions, etc.) -- bail to avoid an infinite loop.
            return


def safe_cache_get(key: str) -> list[dict] | None:
    """Read a cached payload by composite key.

    Returns the list[dict] payload on hit, None on miss/expired/corrupt.
    Never raises.
    """
    path = _filename_for(key)
    try:
        with path.open("r", encoding="utf-8") as f:
            envelope = json.load(f)
    except (OSError, json.JSONDecodeError, ValueError):
        return None

    if not isinstance(envelope, dict):
        return None
    expires_at = envelope.get("expires_at")
    payload = envelope.get("payload")
    if not isinstance(expires_at, (int, float)) or not isinstance(payload, list):
        return None
    if time.time() >= expires_at:
        # Expired -- best-effort unlink; ignore failures.
        try:
            path.unlink()
        except OSError:
            pass
        return None
    return payload


def safe_cache_put(key: str, payload: list[dict]) -> bool:
    """Write a search-result payload to the cache.

    Returns True on success, False on rejection (payload contains a protected
    field). Rejection logs `[cache] refused: payload contains <field>` to stderr.
    """
    rejected = _has_rejected_field(payload)
    if rejected is not None:
        print(
            f"[cache] refused: payload contains {rejected}",
            file=sys.stderr,
        )
        return False

    dir_path = _cache_dir()
    path = _filename_for(key)
    envelope = {
        "key": key,
        "expires_at": time.time() + DEFAULT_TTL_SECONDS,
        "payload": payload,
    }
    try:
        path.write_text(
            json.dumps(envelope, ensure_ascii=False),
            encoding="utf-8",
        )
    except OSError as exc:
        print(f"[cache] write failed: {exc}", file=sys.stderr)
        return False

    # LRU eviction pass (per feasibility P2#2): on every write, enforce the cap.
    cap = int(os.environ.get("META_TOP_CACHE_MAX_BYTES", DEFAULT_MAX_BYTES))
    _evict_to_cap(dir_path, cap)
    return True


__all__ = [
    "REJECTED_FIELDS",
    "DEFAULT_TTL_SECONDS",
    "DEFAULT_MAX_BYTES",
    "safe_cache_get",
    "safe_cache_put",
]