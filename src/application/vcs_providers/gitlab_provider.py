import asyncio
from dataclasses import dataclass, field
from typing import Optional

import gitlab

from application.vcs_providers.base import BaseProvider
from settings import settings


@dataclass
class GitlabProvider(BaseProvider):
    gitlab_client: gitlab.Gitlab = field(init=False)

    def __post_init__(self):
        self.gitlab_client = gitlab.Gitlab(
            url=settings.gitlab_settings.base_url,
            private_token=settings.gitlab_settings.private_token.get_secret_value()
        )


    async def get_code_snippet_from_path(self, project_path: str, file_path: str, mr_id: int, start_line: Optional[int] = None, end_line: Optional[int] = None) -> str:
        """
        Retrieve a code snippet from a file in a merge request.

        :param project_path: The project path (e.g., 'namespace/project').
        :param file_path: The path to the file in the repository.
        :param mr_id: The ID of the merge request.
        :param start_line: Optional start line number for the snippet.
        :param end_line: Optional end line number for the snippet.
        :return: The code snippet as a string.
        """
        return await asyncio.to_thread(self._get_code_snippet_from_path, project_path, file_path, mr_id, start_line, end_line)

    def _get_code_snippet_from_path(self, project_path: str, file_path: str, mr_id: int, start_line: Optional[int] = None, end_line: Optional[int] = None) -> str:
        """
        Synchronous implementation of retrieving a code snippet from a file in a merge request.
        """
        # Get the project
        project = self.gitlab_client.projects.get(project_path)

        # Get the merge request
        mr = project.mergerequests.get(mr_id)

        # Get the source branch of the merge request
        source_branch = mr.source_branch

        # Get the file content from the source branch
        try:
            file_content = project.files.get(file_path, ref=source_branch).decode().splitlines()
        except gitlab.exceptions.GitlabGetError:
            raise ValueError(f"File '{file_path}' not found in branch '{source_branch}'")

        # Extract the snippet based on lines' numbers
        # Extract the snippet based on line numbers
        if start_line is not None and end_line is not None:
            # Validate line numbers
            if start_line < 1 or end_line > len(file_content) or start_line > end_line:
                raise ValueError("Invalid line numbers")

            # Decode each line from bytes to string and extract the snippet
            snippet = "\n".join(line.decode('utf-8').rstrip() for line in file_content[start_line - 1: end_line])
        else:
            # Decode all lines from bytes to string
            snippet = "\n".join(line.decode('utf-8').rstrip() for line in file_content)

        return snippet

    async def publish_code_suggestion(self, code_suggestion: str, project_path: str, discussion_id: str,
                                      mr_id: int) -> None:
        await asyncio.to_thread(self._publish_code_suggestion, code_suggestion, project_path, discussion_id, mr_id)

    def _publish_code_suggestion(self, code_suggestion: str, project_path: str, discussion_id: str, mr_id: int) -> None:
        project = self.gitlab_client.projects.get(project_path)

        # Get the merge request
        mr = project.mergerequests.get(mr_id)

        # Get the specific discussion
        discussion = mr.discussions.get(discussion_id)

        # Add note to the specific discussion
        discussion.notes.create({'body': code_suggestion})
