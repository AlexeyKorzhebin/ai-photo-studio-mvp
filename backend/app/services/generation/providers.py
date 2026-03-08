from dataclasses import dataclass

from backend.app.core.config import settings


@dataclass
class GenerationProviderChoice:
    provider: str
    use_fallback: bool


def resolve_provider(requested: str | None = None) -> GenerationProviderChoice:
    provider = (requested or settings.generation_provider or "auto").strip().lower()
    if provider in {"nano-banana", "gpt-image"} and settings.openai_api_key:
        return GenerationProviderChoice(provider=provider, use_fallback=False)
    return GenerationProviderChoice(provider="fallback", use_fallback=True)
