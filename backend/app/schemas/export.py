from pydantic import BaseModel, Field

from backend.app.schemas.edit_ops import EditOperation


class ExportRequest(BaseModel):
    asset_id: str
    operations: list[EditOperation] = Field(default_factory=list)
    format: str
    quality: int | None = None
