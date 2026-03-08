from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.schemas.export import ExportRequest
from backend.app.services.export_service import ExportService

router = APIRouter(prefix="/api/exports", tags=["exports"])
service = ExportService()


@router.post("")
def export_asset(payload: ExportRequest, db: Session = Depends(get_db)):
    content, media_type = service.export_asset(db, payload)
    ext = payload.format.lower()
    return Response(content=content, media_type=media_type, headers={"Content-Disposition": f'attachment; filename="export.{ext}"'})
