from backend.app.services.image_ops import deterministic_placeholder


def generate_fallback(prompt: str, size: str, style: str | None = None) -> bytes:
    return deterministic_placeholder(prompt=prompt, size=size, style=style)
