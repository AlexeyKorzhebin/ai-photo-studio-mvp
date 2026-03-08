from backend.app.api.errors import AppError


def generate_external(*_, **__):
    raise AppError(503, "External generation provider is not configured in this MVP environment")
