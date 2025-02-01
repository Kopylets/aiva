from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="llm_", extra="ignore")

    api_key: SecretStr
    temperature: float


class LoggerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="log_", extra="ignore")

    name: str
    level: int


class GeneralSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="general_", extra="ignore")

    app_mode: str
