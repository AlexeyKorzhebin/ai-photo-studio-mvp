from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session

from backend.app.api.errors import AppError
from backend.app.models.assets import ImageAsset
from backend.app.schemas.assets import AssetMetadataUpdate
from backend.app.services.asset_repository import AssetRepository
from backend.app.services.image_ops import ALLOWED_MIME_TYPES, probe_image
from backend.app.services.storage_service import StorageService


class AssetService:
    def __init__(self) -> None:
        self.repo = AssetRepository()
        self.storage = StorageService()

    def upload_asset(self, db: Session, upload: UploadFile) -> ImageAsset:
        suffix = Path(upload.filename or "").suffix.lower()
        if suffix not in ALLOWED_MIME_TYPES:
            raise AppError(400, "Unsupported file type. Allowed: png, jpg, jpeg, webp")
        stored_path = self.storage.save_upload(upload)
        try:
            meta = probe_image(stored_path)
        except Exception as exc:
            stored_path.unlink(missing_ok=True)
            raise AppError(400, str(exc)) from exc

        asset = ImageAsset(
            origin_type="upload",
            original_filename=upload.filename or stored_path.name,
            stored_filename=stored_path.name,
            mime_type=meta["mime_type"],
            width=meta["width"],
            height=meta["height"],
            byte_size=meta["byte_size"],
        )
        db.add(asset)
        db.flush()
        metadata = self.repo.ensure_metadata(asset)
        metadata.search_text_normalized = asset.original_filename.lower()
        db.commit()
        db.refresh(asset)
        return asset

    def list_assets(self, db: Session, query: str, sort_by: str, order: str):
        return self.repo.list_assets(db, query=query, sort_by=sort_by, order=order)

    def get_asset(self, db: Session, asset_id: str) -> ImageAsset:
        asset = self.repo.get_asset(db, asset_id)
        if asset is None:
            raise AppError(404, "Asset not found")
        return asset

    def update_metadata(self, db: Session, asset_id: str, payload: AssetMetadataUpdate) -> ImageAsset:
        asset = self.get_asset(db, asset_id)
        metadata = self.repo.ensure_metadata(asset)
        metadata.tags = ",".join(payload.tags)
        metadata.notes = payload.notes
        metadata.search_text_normalized = " ".join([asset.original_filename.lower(), metadata.tags.lower(), metadata.notes.lower()]).strip()
        db.add(asset)
        db.commit()
        db.refresh(asset)
        return asset
