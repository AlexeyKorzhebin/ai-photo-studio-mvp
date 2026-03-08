from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_port: int = 8088
    database_url: str = "sqlite:///./data/app.db"
    asset_storage_dir: Path = Path("./data/assets")
    export_storage_dir: Path = Path("./data/exports")
    generation_provider: str = "auto"
    openai_api_key: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
