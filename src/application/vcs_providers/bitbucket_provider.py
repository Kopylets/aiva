from dataclasses import dataclass

from application.vcs_providers.base import BaseProvider


@dataclass
class BitbucketProvider(BaseProvider):
    async def publish_code_suggestion(self, code_suggestion: str, project_path: str, discussion_id: str) -> None:
        pass

    async def get_code_snippet_from_path(self, path: str) -> str:
        pass
