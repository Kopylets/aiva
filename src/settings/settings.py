from pydantic_settings import BaseSettings

from settings.common import LLMSettings, LoggerSettings, GeneralSettings


class Settings(BaseSettings):
    llm_settings: LLMSettings = LLMSettings()
    logger_settings: LoggerSettings = LoggerSettings()
    general_settings: GeneralSettings = GeneralSettings()
