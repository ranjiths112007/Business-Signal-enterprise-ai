import time
from collections import Counter
from functools import wraps

REQUEST_COUNT = Counter()
REQUEST_LATENCY = {}


def track(name: str):
    def decorator(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            started = time.perf_counter()
            try:
                result = fn(*args, **kwargs)
                REQUEST_COUNT[name] += 1
                return result
            finally:
                REQUEST_LATENCY[name] = round((time.perf_counter() - started) * 1000, 2)
        return wrapped
    return decorator


def snapshot():
    return {"requests": dict(REQUEST_COUNT), "last_latency_ms": REQUEST_LATENCY}
