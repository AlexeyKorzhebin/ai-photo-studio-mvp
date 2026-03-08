from __future__ import annotations

import hashlib
import io
from pathlib import Path
from typing import Any

from PIL import Image, ImageEnhance, ImageOps, ImageDraw

ALLOWED_MIME_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
}
ALLOWED_EXPORT_FORMATS = {"png": "PNG", "jpg": "JPEG", "webp": "WEBP"}


def probe_image(path: Path) -> dict[str, Any]:
    with Image.open(path) as img:
        width, height = img.size
        suffix = path.suffix.lower()
        mime_type = ALLOWED_MIME_TYPES.get(suffix)
        if not mime_type:
            raise ValueError("Unsupported file type")
        return {"width": width, "height": height, "mime_type": mime_type, "byte_size": path.stat().st_size}


def load_image(path: Path) -> Image.Image:
    with Image.open(path) as img:
        return img.convert("RGBA")


def apply_operations(img: Image.Image, operations: list[dict[str, Any]]) -> Image.Image:
    result = img.copy()
    for op in operations:
        kind = op.get("kind")
        params = op.get("params", {})
        if kind == "crop":
            x = int(params.get("x", 0))
            y = int(params.get("y", 0))
            width = int(params.get("width", result.width))
            height = int(params.get("height", result.height))
            result = result.crop((x, y, x + width, y + height))
        elif kind == "rotate":
            degrees = int(params.get("degrees", 0))
            result = result.rotate(-degrees, expand=True)
        elif kind == "flip":
            axis = params.get("axis", "horizontal")
            result = ImageOps.mirror(result) if axis == "horizontal" else ImageOps.flip(result)
        elif kind == "tonal":
            brightness = float(params.get("brightness", 1.0))
            contrast = float(params.get("contrast", 1.0))
            saturation = float(params.get("saturation", 1.0))
            result = ImageEnhance.Brightness(result).enhance(brightness)
            result = ImageEnhance.Contrast(result).enhance(contrast)
            result = ImageEnhance.Color(result).enhance(saturation)
        elif kind == "filter":
            preset = params.get("preset", "none")
            if preset == "grayscale":
                result = ImageOps.grayscale(result).convert("RGBA")
            elif preset == "sepia":
                gray = ImageOps.grayscale(result)
                result = ImageOps.colorize(gray, "#704214", "#f4ecd8").convert("RGBA")
    return result


def encode_image(img: Image.Image, fmt: str, quality: int | None = None) -> bytes:
    output = io.BytesIO()
    fmt_key = fmt.lower()
    pil_fmt = ALLOWED_EXPORT_FORMATS[fmt_key]
    save_image = img.convert("RGB") if pil_fmt in {"JPEG", "WEBP"} else img
    kwargs: dict[str, Any] = {}
    if quality and pil_fmt in {"JPEG", "WEBP"}:
        kwargs["quality"] = quality
    save_image.save(output, format=pil_fmt, **kwargs)
    return output.getvalue()


def deterministic_placeholder(prompt: str, size: str, style: str | None = None) -> bytes:
    width, height = [int(x) for x in size.split("x")]
    normalized = f"{prompt.strip().lower()}|{size}|{(style or '').strip().lower()}"
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    bg = f"#{digest[:6]}"
    fg = f"#{digest[6:12]}"
    img = Image.new("RGBA", (width, height), bg)
    draw = ImageDraw.Draw(img)
    for idx in range(0, min(width, height), max(24, min(width, height) // 8)):
        draw.rectangle((idx, idx, width - idx // 2 - 1, height - idx // 2 - 1), outline=fg, width=4)
    draw.text((24, 24), prompt[:80], fill=fg)
    return encode_image(img, "png")
