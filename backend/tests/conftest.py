from pathlib import Path
import shutil

import pytest
from fastapi.testclient import TestClient

from backend.app.core.config import settings
from backend.app.main import app
from backend.app.db.init_db import init_db


@pytest.fixture(autouse=True)
def clean_storage():
    for folder in [Path(settings.asset_storage_dir), Path(settings.export_storage_dir)]:
        folder.mkdir(parents=True, exist_ok=True)
        for entry in folder.iterdir():
            if entry.is_file() and entry.name != ".gitkeep":
                entry.unlink()
    db_path = Path("data/app.db")
    if db_path.exists():
        db_path.unlink()
    init_db()
    yield


@pytest.fixture()
def client():
    return TestClient(app)
