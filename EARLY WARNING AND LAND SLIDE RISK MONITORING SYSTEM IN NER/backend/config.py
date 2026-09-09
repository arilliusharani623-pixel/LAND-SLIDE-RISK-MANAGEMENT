import os
from pathlib import Path

from functools import lru_cache


def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        key, separator, value = line.partition("=")
        if separator and key.strip() and key.strip() not in os.environ:
            os.environ[key.strip()] = value.strip().strip('"').strip("'")


class Settings:
    def __init__(self) -> None:
        _load_dotenv(Path(__file__).resolve().parent / ".env")
        self.app_name = os.getenv("APP_NAME", "Landslide Risk Prediction API")
        self.environment = os.getenv("ENVIRONMENT", "development")
        configured_model_path = os.getenv("MODEL_PATH", "model.pkl")
        self.model_path = Path(configured_model_path)
        if not self.model_path.is_absolute():
            self.model_path = Path(__file__).resolve().parent / self.model_path
        self.allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
