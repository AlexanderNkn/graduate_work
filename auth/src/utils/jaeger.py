from functools import wraps

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
        with tracer.start_span(operation_name=fn.__name__, child_of=parent_span):
            return fn(*args, **kwargs)

    return wrapper
