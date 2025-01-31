from dataclasses import dataclass

from application.vcs_providers import BaseProvider

from .base import BaseCodeSuggestService


@dataclass
class CodeSuggestService(BaseCodeSuggestService):
    vcs_provider: BaseProvider

    async def suggest_code(self, comment: str) -> None:
        comment = await self._suggest_code(comment=comment)
        # do smth with vcs provider
        print(self.vcs_provider.__class__.__name__)

    @classmethod
    async def _suggest_code(cls, comment: str) -> str:
        return "lambda x: x + 1"
