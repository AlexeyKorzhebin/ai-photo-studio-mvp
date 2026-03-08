from __future__ import annotations

import hashlib
import io
import json
from abc import ABC, abstractmethod

from PIL import Image, ImageDraw

from app.core.config import settings


class GenerationResult:
    def __init__(
        self,
        image_bytes: bytes,
        mime_type: str,
        provider_used: str,
        fallback_used: bool,
        is_mock: bool,
        seed_hash: str,
    ) -> None:
        self.image_bytes = image_bytes
        self.mime_type = mime_type
        self.provider_used = provider_used
        self.fallback_used = fallback_used
        self.is_mock = is_mock
        self.seed_hash = seed_hash


class BaseProvider(ABC):
    @abstractmethod
    def generate(
        self,
        prompt: str,
        size: str,
        width: int,
        height: int,
        style: str | None,
        provider_override: str | None,
    ) -> GenerationResult:
        raise NotImplementedError


def _normalize_text(value: str | None) -> str:
    if not value:
        return ""
    return " ".join(value.split())


def _normalize_seed_input(
    prompt: str,
    size: str,
    style: str | None,
    provider_override: str | None,
) -> tuple[str, str, str, str, str]:
    normalized_override = _normalize_text(provider_override).lower()
    override_intent = "set" if normalized_override else "unset"
    return (
        _normalize_text(prompt),
        size.strip().lower(),
        _normalize_text(style),
        override_intent,
        normalized_override,
    )


def _seed_hash_for_input(
    prompt: str,
    size: str,
    style: str | None,
    provider_override: str | None,
) -> tuple[str, str]:
    normalized = _normalize_seed_input(prompt, size, style, provider_override)
    serialized = json.dumps(normalized, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest(), normalized[0]


def _mock_image(seed_hash: str, normalized_prompt: str, width: int, height: int, label: str) -> bytes:
    bg = tuple(int(seed_hash[i : i + 2], 16) for i in (0, 2, 4))
    fg = tuple(255 - c for c in bg)

    img = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(img)
    text = f"{label}\n{normalized_prompt[:70]}\n{seed_hash[:12]}"
    draw.rectangle([(30, 30), (width - 30, height - 30)], outline=fg, width=6)
    draw.text((48, 48), text, fill=fg)
    out = io.BytesIO()
    img.save(out, format="PNG")
    return out.getvalue()


class MockProvider(BaseProvider):
    def __init__(self, fallback_used: bool = False) -> None:
        self._fallback_used = fallback_used

    def generate(
        self,
        prompt: str,
        size: str,
        width: int,
        height: int,
        style: str | None,
        provider_override: str | None,
    ) -> GenerationResult:
        seed_hash, normalized_prompt = _seed_hash_for_input(prompt, size, style, provider_override)
        return GenerationResult(
            image_bytes=_mock_image(seed_hash, normalized_prompt, width, height, "MOCK"),
            mime_type="image/png",
            provider_used="mock",
            fallback_used=self._fallback_used,
            is_mock=True,
            seed_hash=seed_hash,
        )


class NanoBananaProvider(BaseProvider):
    def generate(
        self,
        prompt: str,
        size: str,
        width: int,
        height: int,
        style: str | None,
        provider_override: str | None,
    ) -> GenerationResult:
        if not settings.nano_banana_api_key:
            return MockProvider(fallback_used=True).generate(prompt, size, width, height, style, provider_override)
        seed_hash, normalized_prompt = _seed_hash_for_input(prompt, size, style, provider_override)
        # Placeholder for real integration.
        return GenerationResult(
            image_bytes=_mock_image(seed_hash, normalized_prompt, width, height, "NANO-BANANA"),
            mime_type="image/png",
            provider_used="nano-banana",
            fallback_used=False,
            is_mock=False,
            seed_hash=seed_hash,
        )


class GPTImageProvider(BaseProvider):
    def generate(
        self,
        prompt: str,
        size: str,
        width: int,
        height: int,
        style: str | None,
        provider_override: str | None,
    ) -> GenerationResult:
        if not settings.gpt_image_api_key:
            return MockProvider(fallback_used=True).generate(prompt, size, width, height, style, provider_override)
        seed_hash, normalized_prompt = _seed_hash_for_input(prompt, size, style, provider_override)
        # Placeholder for real integration.
        return GenerationResult(
            image_bytes=_mock_image(seed_hash, normalized_prompt, width, height, "GPT-IMAGE"),
            mime_type="image/png",
            provider_used="gpt-image",
            fallback_used=False,
            is_mock=False,
            seed_hash=seed_hash,
        )


def resolve_provider(override: str | None = None) -> BaseProvider:
    requested = (override or settings.ai_provider or "mock").strip().lower()
    if requested == "nano-banana":
        return NanoBananaProvider()
    if requested == "gpt-image":
        return GPTImageProvider()
    return MockProvider()
