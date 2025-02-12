from pathlib import Path
from typing import Annotated, TypeAlias, Sequence

from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from pydantic import BaseModel, Field, AfterValidator, computed_field
from pydantic_settings import BaseSettings, TomlConfigSettingsSource


def prepare_prompt(value: str | None) -> str:
    return value.strip() if value is not None else value


PromptType: TypeAlias = Annotated[str | None, AfterValidator(prepare_prompt)]


class BaseGigaChatPrompt(BaseModel):
    system: PromptType = Field(default=None)
    user: PromptType = Field(default=None)

    @computed_field
    def messages(self) -> Sequence[BaseMessage] | None:
        messages = []
        if self.system:
            messages.append(SystemMessage(content=self.system))
        if self.user:
            messages.append(HumanMessage(content=self.user))
        return messages if len(messages) != 0 else None


class GigaChatPrompts(BaseSettings):
    base_prompt: BaseGigaChatPrompt
    generate_code_request: BaseGigaChatPrompt
    validate_code_request: BaseGigaChatPrompt

    mr_summary_prompt: BaseGigaChatPrompt

    @classmethod
    def settings_customise_sources(cls, settings_cls, **kwargs):
        base_path = Path(__file__).parent
        return (
            TomlConfigSettingsSource(
                settings_cls,
                [
                    base_path / prompt_path
                    for prompt_path in [
                        Path("templates/comment_code_suggest_prompts.toml"),
                        Path("templates/mr_summary_prompt.toml"),
                    ]
                ],
            ),
        )
