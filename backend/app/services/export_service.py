from backend.app.api.errors import AppError
from backend.app.schemas.export import ExportRequest
from backend.app.services.asset_service import AssetService
from backend.app.services.image_ops import ALLOWED_EXPORT_FORMATS, apply_operations, encode_image, load_image
from sqlalchemy.orm import Session


class ExportService:
    def __init__(self) -> None:
        self.assets = AssetService()

    def export_asset(self, db: Session, payload: ExportRequest) -> tuple[bytes, str]:
        asset = self.assets.get_asset(db, payload.asset_id)
        if payload.format.lower() not in ALLOWED_EXPORT_FORMATS:
            raise AppError(400, "Unsupported export format")
        if payload.format.lower() in {"jpg", "webp"} and payload.quality is None:
            raise AppError(400, "Quality is required for jpg/webp")
        image = load_image(self.assets.storage.asset_path(asset.stored_filename))
        image = apply_operations(image, [op.model_dump() for op in payload.operations])
        mime = {"png": "image/png", "jpg": "image/jpeg", "webp": "image/webp"}[payload.format.lower()]
        return encode_image(image, payload.format, payload.quality), mime
