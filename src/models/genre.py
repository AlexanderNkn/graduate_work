import uuid
from typing import Optional

from .base import BaseModel


class Genre(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str]
