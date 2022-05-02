import logging
from functools import wraps
from logging import config
from time import sleep

from .logging_config import LOGGING_CONFIG

config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('backoff')


def backoff(exception, initial_backoff=1, factor=2, max_backoff=600, max_retries=1, msg=None):
    """
    This decorator is used to retry function with exponential time if specific
    exception was met.

    To do this it will wait by calling time.sleep for ``initial_backoff`` seconds
    and then, every subsequent rejection, for double the time every time
    up to ``max_backoff`` seconds.

    :arg exception exception if raised retries decorated function
    :arg initial_backoff: number of seconds we should wait before the first
        retry. Any subsequent retries will be powers of ``initial_backoff *
        factor**retry_number``
    :arg max_backoff: maximum number of seconds a retry will wait
    :arg max_retries: maximum number of times a document will be retried
    :arg msg: default message if exception raised
    """
    def func_wrapper(func):
        @wraps(func)
        def retry(*args, **kwargs):
            result = None
            retry_number = 0
            while retry_number < max_retries:
                try:
                    result = func(*args, **kwargs)
                except exception:
                    if msg is not None:
                        logger.info(msg=msg)
                    delay = initial_backoff * factor ** retry_number
                    max_delay = delay if delay < max_backoff else max_backoff
                    logger.info(f'Try to reconnect after {max_delay} seconds')
                    sleep(max_delay)
                    retry_number += 1
                    continue
                else:
                    break
            if result is not None:
                return result
            raise exception
        return retry
    return func_wrapper
