"""Lightweight in-process request metrics used by the /metrics health endpoint."""
import time
from typing import Any

_started_at: float = time.time()
_counters: dict[str, int] = {"requests": 0, "errors": 0}


def record_request(error: bool = False) -> None:
    _counters["requests"] += 1
    if error:
        _counters["errors"] += 1


def snapshot() -> dict[str, Any]:
    uptime = round(time.time() - _started_at, 1)
    return {
        "uptime_seconds": uptime,
        "requests_total": _counters["requests"],
        "errors_total": _counters["errors"],
    }
