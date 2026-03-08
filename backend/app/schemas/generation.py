from pydantic import BaseModel, Field


class GenerationRequest(BaseModel):
    prompt: str = Field(min_length=1)
    size: str
    style: str | None = None
    provider: str | None = None


class GenerationResponse(BaseModel):
    asset_id: str
    provider: str
