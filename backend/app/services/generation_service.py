from pathlib import Path
import uuid

from sqlalchemy.orm import Session

from backend.app.models.assets import ImageAsset
from backend.app.schemas.generation import GenerationRequest
from backend.app.services.asset_repository import AssetRepository
from backend.app.services.generation.external_providers import generate_external
from backend.app.services.generation.fallback_provider import generate_fallback
from backend.app.services.generation.providers import resolve_provider
from backend.app.services.image_ops import probe_image
from backend.app.services.storage_service import StorageService

ALLOWED_SIZES = {"1024x1024", "1024x1536", "1536x1024"}


class GenerationService:
    def __init__(self) -> None:
        self.repo = AssetRepository()
        self.storage = StorageService()

    def generate(self, db: Session, payload: GenerationRequest) -> tuple[ImageAsset, str]:
        if payload.size not in ALLOWED_SIZES:
            raise ValueError("Unsupported generation size")
        choice = resolve_provider(payload.provider)
        image_bytes = generate_fallback(payload.prompt, payload.size, payload.style) if choice.use_fallback else generate_external(payload)
        target = self.storage.asset_path(f"{uuid.uuid4()}.png")
        target.write_bytes(image_bytes)
        meta = probe_image(target)
        asset = ImageAsset(
            origin_type="generated",
            original_filename=f"generated-{payload.prompt[:24] or 'image'}.png",
            stored_filename=target.name,
            mime_type=meta["mime_type"],
            width=meta["width"],
            height=meta["height"],
            byte_size=meta["byte_size"],
        )
        db.add(asset)
        db.flush()
        metadata = self.repo.ensure_metadata(asset)
        metadata.search_text_normalized = f"generated {payload.prompt.lower()} {(payload.style or '').lower()}"
        db.commit()
        db.refresh(asset)
        return asset, choice.provider
