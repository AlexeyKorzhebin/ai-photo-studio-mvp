from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse


class AppError(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(_, exc: AppError):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(HTTPException)
    async def handle_http_error(_, exc: HTTPException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
