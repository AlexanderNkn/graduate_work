from functools import wraps
from time import sleep

from .logger import Logger

logger = Logger(__name__)


def backoff(exception, initial_backoff=0.1, factor=2, max_backoff=10):
    """
    This decorator is used to retry function with exponential time if specific
    exception was met.

    To do this it will wait by calling time.sleep for ``initial_backoff`` seconds
    and then, every subsequent rejection, for double the time every time
    up to ``max_backoff`` seconds.
    """
    def func_wrapper(func):
        @wraps(func)
        def retry(*args, **kwargs):
            attempt = 0
            while True:
                try:
                    result = func(*args, **kwargs)
                except exception:
                    delay = initial_backoff * factor ** attempt
                    max_delay = delay if delay < max_backoff else max_backoff
                    logger.info(f'Try to reconnect after {max_delay} seconds')
                    sleep(max_delay)
                    attempt += 1
                    continue
                else:
                    break
            return result
        return retry
    return func_wrapper
