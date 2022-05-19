from functools import wraps

from flask import request
from opentracing import global_tracer


def trace(fn):
    """This decorator is used for distributed tracing of internal methods that
    doesn't handle with default tracing process.

    Using:
        @trace
        def some_function():
            pass
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        tracer = global_tracer()
        parent_span = tracer.active_span
        request_id = request.headers.get('X-Request-Id')
        parent_span.set_tag('http.request.header.x_request_id', f"('{request_id}',)")
        with tracer.start_span(operation_name=fn.__name__, child_of=parent_span):
            return fn(*args, **kwargs)

    return wrapper
