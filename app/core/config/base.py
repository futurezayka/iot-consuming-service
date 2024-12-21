from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

__all__ = ["BaseConfig"]


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )
