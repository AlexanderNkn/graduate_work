from functools import wraps
from time import sleep


def backoff(initial_backoff=0.1, factor=2, max_backoff=10):
    """
    Function repeatedly calls another function.

    To do this it will wait by calling time.sleep for ``initial_backoff`` seconds
    and then, every subsequent rejection, for double the time every time
    up to ``max_backoff`` seconds.
    """
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            attempt = 0
            while not result:
                delay = initial_backoff * factor ** attempt
                max_delay = delay if delay < max_backoff else max_backoff
                print(f'time to sleep {max_delay}')
                sleep(max_delay)
                result = func(*args, **kwargs)
                attempt += 1
            return result
        return inner
    return func_wrapper
