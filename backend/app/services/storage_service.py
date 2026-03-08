from pathlib import Path
import shutil
import uuid

from fastapi import UploadFile

from backend.app.core.config import settings


class StorageService:
    def __init__(self) -> None:
        self.asset_dir = Path(settings.asset_storage_dir)
        self.export_dir = Path(settings.export_storage_dir)
        self.asset_dir.mkdir(parents=True, exist_ok=True)
        self.export_dir.mkdir(parents=True, exist_ok=True)

    def save_upload(self, upload: UploadFile) -> Path:
        suffix = Path(upload.filename or "image").suffix.lower() or ".bin"
        target = self.asset_dir / f"{uuid.uuid4()}{suffix}"
        with target.open("wb") as buffer:
            shutil.copyfileobj(upload.file, buffer)
        upload.file.seek(0)
        return target

    def asset_path(self, stored_filename: str) -> Path:
        return self.asset_dir / stored_filename

    def export_path(self, filename: str) -> Path:
        return self.export_dir / filename
