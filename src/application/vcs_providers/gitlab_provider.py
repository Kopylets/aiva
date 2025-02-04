import asyncio
from dataclasses import dataclass, field

import gitlab

from application.vcs_providers.base import BaseProvider
from settings import settings


@dataclass
class GitlabProvider(BaseProvider):
    gitlab_client: gitlab.Gitlab = field(init=False)

    def __post_init__(self):
        self.gitlab_client = gitlab.Gitlab(
            url=settings.gitlab_settings.base_url,
            private_token=settings.gitlab_settings.private_token
        )

    async def get_code_snippet_from_path(self, path: str) -> str:
        return 'print("123")'

    async def publish_code_suggestion(self, code_suggestion: str, project_path: str, discussion_id: str) -> None:
        await asyncio.to_thread(self._publish_code_suggestion, code_suggestion, project_path, discussion_id)

    def _publish_code_suggestion(self, code_suggestion: str, project_path: str, discussion_id: str) -> None:
        project = self.gitlab_client.projects.get(project_path)

        # Get the merge request
        mr = project.mergerequests.get(4)

        # Get the specific discussion
        discussion = mr.discussions.get(discussion_id)

        # Add note to the specific discussion
        discussion.notes.create({'body': code_suggestion})
