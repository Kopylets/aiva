from dataclasses import dataclass

from application.vcs_providers.base import BaseProvider


@dataclass
class GitlabProvider(BaseProvider):
    async def publish_code_suggestions(self, code_suggestions: list) -> bool:
        pass
