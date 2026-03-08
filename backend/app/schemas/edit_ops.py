from typing import Literal, Any

from pydantic import BaseModel, Field


class EditOperation(BaseModel):
    kind: Literal["crop", "rotate", "flip", "tonal", "filter"]
    params: dict[str, Any] = Field(default_factory=dict)
