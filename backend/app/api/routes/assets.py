from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.schemas.assets import AssetListResponse, AssetMetadataResponse, AssetMetadataUpdate, ImageAssetResponse
from backend.app.services.asset_service import AssetService

router = APIRouter(prefix="/api/assets", tags=["assets"])
service = AssetService()


def serialize(asset):
    metadata = asset.metadata_entry
    tags = metadata.tags.split(",") if metadata and metadata.tags else []
    return ImageAssetResponse(
        id=asset.id,
        origin_type=asset.origin_type,
        original_filename=asset.original_filename,
        stored_filename=asset.stored_filename,
        mime_type=asset.mime_type,
        width=asset.width,
        height=asset.height,
        byte_size=asset.byte_size,
        created_at=asset.created_at,
        updated_at=asset.updated_at,
        metadata=AssetMetadataResponse(tags=tags, notes=metadata.notes if metadata else ""),
    )


@router.post("/upload", response_model=ImageAssetResponse, status_code=201)
def upload_asset(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return serialize(service.upload_asset(db, file))


@router.get("", response_model=AssetListResponse)
def list_assets(q: str = "", sortBy: str = "updated_at", order: str = "desc", db: Session = Depends(get_db)):
    items = [serialize(asset) for asset in service.list_assets(db, q, sortBy, order)]
    return AssetListResponse(items=items)


@router.get("/{asset_id}", response_model=ImageAssetResponse)
def get_asset(asset_id: str, db: Session = Depends(get_db)):
    return serialize(service.get_asset(db, asset_id))


@router.patch("/{asset_id}/metadata", response_model=ImageAssetResponse)
def patch_asset_metadata(asset_id: str, payload: AssetMetadataUpdate, db: Session = Depends(get_db)):
    return serialize(service.update_metadata(db, asset_id, payload))


@router.get("/{asset_id}/binary")
def get_asset_binary(asset_id: str, db: Session = Depends(get_db)):
    asset = service.get_asset(db, asset_id)
    return FileResponse(service.storage.asset_path(asset.stored_filename), media_type=asset.mime_type, filename=asset.original_filename)
