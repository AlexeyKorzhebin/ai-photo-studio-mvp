from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ImageOut(BaseModel):
    id: int
    filename: str
    mime_type: str
    size_bytes: int
    width: int
    height: int
    source_type: str
    provider: str | None
    prompt: str | None
    tags: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime
    file_url: str

    model_config = {"from_attributes": True}


class ImageListOut(BaseModel):
    items: list[ImageOut]


class ImageUpdateIn(BaseModel):
    tags: str | None = Field(default=None)
    notes: str | None = Field(default=None)


class AIGenerateIn(BaseModel):
    prompt: str = Field(min_length=1, max_length=1000)
    size: Literal["1024x1024", "1024x1536", "1536x1024"] = "1024x1024"
    style: str | None = Field(default=None, max_length=120)
    provider: str | None = Field(default=None, max_length=32)


class AIGenerateOut(BaseModel):
    image: ImageOut
    provider_used: str
    fallback_used: bool
