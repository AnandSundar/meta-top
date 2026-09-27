"""Minimal stdlib-only HTTP helpers used by meta-top's keyless search floor.

Last30days's lib/http.py is a 14KB beast with full auth/cookie/rate-limit
support. For meta-top's floor tier (no auth, no cookies, simple GET with
backoff) we keep the surface tight to reduce maintenance.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request

DEFAULT_TIMEOUT = 30
DEFAULT_RETRIES = 2
BACKOFF_BASE = 1.5

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


class HTTPError(Exception):
    """Surface non-200/non-3xx responses as a soft error rather than raising."""


def _request(url: str, headers: dict, timeout: int, retries: int) -> bytes:
    """GET with simple exponential backoff. Returns response body bytes."""
    merged = {"User-Agent": USER_AGENT, **headers}
    last_err: Exception | None = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=merged, method="GET")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                if 200 <= resp.status < 400:
                    return resp.read()
                last_err = HTTPError(f"HTTP {resp.status} for {url}")
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
            last_err = exc
        if attempt < retries:
            time.sleep(BACKOFF_BASE ** attempt)
    raise last_err if last_err else HTTPError(f"No response for {url}")


def get_text(
    url: str,
    *,
    accept: str = "*/*",
    retries: int = DEFAULT_RETRIES,
    timeout: int = DEFAULT_TIMEOUT,
) -> str:
    """GET and decode as UTF-8 text. Empty string on total failure (never raises)."""
    try:
        body = _request(url, {"Accept": accept}, timeout=timeout, retries=retries)
        return body.decode("utf-8", errors="replace")
    except Exception:
        return ""


def get(
    url: str,
    *,
    headers: dict | None = None,
    retries: int = DEFAULT_RETRIES,
    timeout: int = DEFAULT_TIMEOUT,
):
    """GET and parse as JSON. Returns dict/list or None on total failure."""
    try:
        body = _request(
            url,
            headers or {"Accept": "application/json"},
            timeout=timeout,
            retries=retries,
        )
        return json.loads(body.decode("utf-8", errors="replace"))
    except Exception:
        return None
