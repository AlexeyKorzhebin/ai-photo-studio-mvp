from datetime import datetime

from pydantic import BaseModel, Field


class AssetMetadataUpdate(BaseModel):
    tags: list[str] = Field(default_factory=list)
    notes: str = ""


class AssetMetadataResponse(BaseModel):
    tags: list[str] = Field(default_factory=list)
    notes: str = ""


class ImageAssetResponse(BaseModel):
    id: str
    origin_type: str
    original_filename: str
    stored_filename: str
    mime_type: str
    width: int
    height: int
    byte_size: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
    metadata: AssetMetadataResponse


class AssetListResponse(BaseModel):
    items: list[ImageAssetResponse]
