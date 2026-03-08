from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app.api.errors import AppError
from backend.app.db.session import get_db
from backend.app.schemas.generation import GenerationRequest, GenerationResponse
from backend.app.services.generation_service import GenerationService

router = APIRouter(prefix="/api/generation", tags=["generation"])
service = GenerationService()


@router.post("", response_model=GenerationResponse)
def generate(payload: GenerationRequest, db: Session = Depends(get_db)):
    try:
        asset, provider = service.generate(db, payload)
    except ValueError as exc:
        raise AppError(400, str(exc)) from exc
    return GenerationResponse(asset_id=asset.id, provider=provider)
