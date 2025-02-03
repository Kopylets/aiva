from pydantic_settings import BaseSettings

from settings.common import LLMSettings, LoggerSettings, GeneralSettings, LogfireSettings


class Settings(BaseSettings):
    llm_settings: LLMSettings = LLMSettings()
    logger_settings: LoggerSettings = LoggerSettings()
    logfire_settings: LogfireSettings = LogfireSettings()
    general_settings: GeneralSettings = GeneralSettings()
