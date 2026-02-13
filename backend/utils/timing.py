import time
from contextlib import contextmanager
from typing import Generator


@contextmanager
def timer() -> Generator[dict, None, None]:
    """
    Context manager that measures elapsed wall-clock time in milliseconds.

    Usage:
        with timer() as t:
            do_work()
        print(t["elapsed_ms"])
    """
    result: dict = {"elapsed_ms": 0.0}
    start = time.perf_counter()
    try:
        yield result
    finally:
        end = time.perf_counter()
        result["elapsed_ms"] = round((end - start) * 1000, 2)
