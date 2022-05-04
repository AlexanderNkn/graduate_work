import datetime
from hashlib import sha1

from flask import request
from werkzeug.exceptions import TooManyRequests

from extensions import cache


def check_request_id() -> None:
    """This is mandatory header for requests tracing"""
    if not request.headers.get('X-Request-Id'):
        raise RuntimeError('request id is requred')


def check_rate_limit(limit: int) -> None:
    """Restricts number of user requests using Token Bucket algorithm."""
    ip = request.remote_addr
    user_agent = request.user_agent.string
    user_identity = sha1((str(ip) + user_agent).encode()).hexdigest()
    now = datetime.datetime.now()
    key = f'{user_identity}:{now.minute}'

    # explicit call redis backend to have possibility to use inc() method
    redis_cache = cache.cache
    request_number = redis_cache.get(key)
    if request_number is None:
        redis_cache.set(key=key, value=1, timeout=59)
        request_number = 1
    # increment key at once to get actual request_number on next request
    redis_cache.inc(key)

    if request_number > limit:
        raise TooManyRequests
