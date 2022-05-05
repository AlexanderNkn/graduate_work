import orjson
from pydantic import BaseModel as PydanticBaseModel


def orjson_dumps(value, *, default=None):
    return orjson.dumps(value, default=default).decode()


class BaseModel(PydanticBaseModel):
    """Default pydantic model was extended by improved json methods."""

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
