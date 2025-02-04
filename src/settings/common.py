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


class LogfireSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="logfire_", extra="ignore")

    token: SecretStr
    console: bool
    service_name: str
    send_to_logfire: bool


class GitLabSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="gitlab_", extra="ignore")

    base_url: str
    private_token: SecretStr


class GeneralSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="general_", extra="ignore")

    app_mode: str
