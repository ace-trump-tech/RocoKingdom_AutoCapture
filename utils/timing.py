# utils/timing.py
import time
import functools
from typing import Callable

class Timer:
    """Context manager for measuring elapsed time."""
    def __enter__(self):
        self.start = time.perf_counter()
        return self
    
    def __exit__(self, *args):
        self.end = time.perf_counter()
        self.elapsed = self.end - self.start
    
    def get_elapsed(self) -> float:
        return self.elapsed

def timeit(func: Callable) -> Callable:
    """
    Decorator to log function execution time.
    Requires a logger named __name__ to be available.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        # Try to get logger; if not available, print
        try:
            import logging
            logger = logging.getLogger(func.__module__)
            logger.debug(f"{func.__name__} took {elapsed:.4f} seconds")
        except Exception:
            print(f"{func.__name__} took {elapsed:.4f} seconds")
        return result
    return wrapper

def sleep_with_jitter(seconds: float, jitter: float = 0.1):
    """
    Sleep for a given time plus random jitter to avoid detection.
    """
    import random
    actual = seconds + random.uniform(-jitter, jitter)
    if actual < 0:
        actual = 0
    time.sleep(actual)
