import datetime
from hashlib import sha1

import redis
from flask import request
from werkzeug.exceptions import TooManyRequests

from core.config import REDIS_HOST, REDIS_PORT

redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


def check_request_id() -> None:
    """This is mandatory header for requests tracing"""
    if not request.headers.get('X-Request-Id'):
        raise RuntimeError('request id is requred')


def check_rate_limit(limit: int) -> None:
    """Restricts number of user requests using Token Bucket algorithm."""
    ip = request.remote_addr
    user_agent = request.user_agent.string
    user_identity = sha1((ip + user_agent).encode()).hexdigest()

    pipe = redis_conn.pipeline()
    now = datetime.datetime.now()
    key = f'{user_identity}:{now.minute}'
    pipe.incr(key, 1)
    pipe.expire(key, 59)
    result = pipe.execute()
    request_number = result[0]
    if request_number > limit:
        raise TooManyRequests
