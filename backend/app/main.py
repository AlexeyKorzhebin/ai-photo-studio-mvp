from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.app.api.errors import install_error_handlers
from backend.app.api.routes.assets import router as assets_router
from backend.app.api.routes.exports import router as exports_router
from backend.app.api.routes.generation import router as generation_router
from backend.app.api.routes.health import router as health_router
from backend.app.db.init_db import init_db

app = FastAPI(title="AI Photo Studio MVP", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
install_error_handlers(app)
app.include_router(health_router)
app.include_router(assets_router)
app.include_router(exports_router)
app.include_router(generation_router)


@app.on_event("startup")
def startup() -> None:
    init_db()


frontend_dist = Path("frontend/dist")
if frontend_dist.exists():
    app.mount("/assets", StaticFiles(directory=frontend_dist / "assets"), name="frontend-assets")

    @app.get("/{path:path}")
    def serve_spa(path: str):
        if path.startswith("api/"):
            return {"detail": "Not found"}
        index_path = frontend_dist / "index.html"
        return FileResponse(index_path)
