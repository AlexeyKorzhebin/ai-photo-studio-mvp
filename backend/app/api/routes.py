from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.image import ImageAsset
from app.schemas.image import AIGenerateIn, AIGenerateOut, ImageListOut, ImageOut, ImageUpdateIn
from app.services.ai_providers import resolve_provider
from app.services.storage import StorageService

router = APIRouter()
storage = StorageService()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


def to_out(image: ImageAsset) -> ImageOut:
    return ImageOut(
        id=image.id,
        filename=image.filename,
        mime_type=image.mime_type,
        size_bytes=image.size_bytes,
        width=image.width,
        height=image.height,
        source_type=image.source_type,
        provider=image.provider,
        prompt=image.prompt,
        is_mock=image.is_mock,
        seed_hash=image.seed_hash,
        tags=image.tags,
        notes=image.notes,
        created_at=image.created_at,
        updated_at=image.updated_at,
        file_url=f"/api/images/{image.id}/file",
    )


@router.get("/images", response_model=ImageListOut)
def list_images(
    search: str | None = Query(default=None),
    sort: str = Query(default="created_at"),
    order: str = Query(default="desc"),
    db: Session = Depends(get_db),
) -> ImageListOut:
    sort_map = {
        "created_at": ImageAsset.created_at,
        "updated_at": ImageAsset.updated_at,
        "name": ImageAsset.filename,
    }
    column = sort_map.get(sort, ImageAsset.created_at)
    descending = order.lower() == "desc"
    primary_order = desc(column) if descending else asc(column)
    secondary_order = desc(ImageAsset.id) if descending else asc(ImageAsset.id)

    q = db.query(ImageAsset)
    if search:
        terms = [term.strip() for term in search.split() if term.strip()]
        for term in terms:
            like = f"%{term}%"
            q = q.filter(
                or_(
                    ImageAsset.filename.ilike(like),
                    ImageAsset.tags.ilike(like),
                    ImageAsset.notes.ilike(like),
                )
            )

    items = q.order_by(primary_order, secondary_order).all()
    return ImageListOut(items=[to_out(item) for item in items])


@router.post("/images/upload", response_model=ImageOut)
def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)) -> ImageOut:
    try:
        stored_name, size_bytes, width, height, mime_type = storage.save_upload(file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    image = ImageAsset(
        filename=file.filename or "uploaded-image",
        stored_name=stored_name,
        mime_type=mime_type,
        size_bytes=size_bytes,
        width=width,
        height=height,
        source_type="upload",
    )
    db.add(image)
    db.commit()
    db.refresh(image)
    return to_out(image)


@router.get("/images/{image_id}", response_model=ImageOut)
def get_image(image_id: int, db: Session = Depends(get_db)) -> ImageOut:
    image = db.get(ImageAsset, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return to_out(image)


@router.get("/images/{image_id}/file")
def get_image_file(image_id: int, db: Session = Depends(get_db)) -> FileResponse:
    image = db.get(ImageAsset, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    path = storage.get_path(image.stored_name)
    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=path, media_type=image.mime_type, filename=image.filename)


@router.patch("/images/{image_id}", response_model=ImageOut)
def update_image(image_id: int, payload: ImageUpdateIn, db: Session = Depends(get_db)) -> ImageOut:
    image = db.get(ImageAsset, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    image.tags = payload.tags
    image.notes = payload.notes
    db.add(image)
    db.commit()
    db.refresh(image)
    return to_out(image)


@router.post("/ai/generate", response_model=AIGenerateOut)
def generate_image(payload: AIGenerateIn, db: Session = Depends(get_db)) -> AIGenerateOut:
    size_to_dimensions = {
        "1024x1024": (1024, 1024),
        "1024x1536": (1024, 1536),
        "1536x1024": (1536, 1024),
    }
    width, height = size_to_dimensions[payload.size]
    provider = resolve_provider(payload.provider)
    result = provider.generate(payload.prompt, payload.size, width, height, payload.style, payload.provider)
    stored_name, size_bytes, width, height = storage.save_generated(result.image_bytes, result.mime_type)

    image = ImageAsset(
        filename=f"ai-{payload.prompt[:18].strip().replace(' ', '-') or 'image'}.png",
        stored_name=stored_name,
        mime_type=result.mime_type,
        size_bytes=size_bytes,
        width=width,
        height=height,
        source_type="generated",
        provider=result.provider_used,
        prompt=payload.prompt,
        is_mock=result.is_mock,
        seed_hash=result.seed_hash,
    )
    db.add(image)
    db.commit()
    db.refresh(image)

    return AIGenerateOut(
        image=to_out(image),
        provider_used=result.provider_used,
        fallback_used=result.fallback_used,
        seed_hash=result.seed_hash,
    )
