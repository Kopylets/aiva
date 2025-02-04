from abc import ABC, abstractmethod


class BaseProvider(ABC):
    @abstractmethod
    async def publish_code_suggestion(self, code_suggestion: str, project_path: str, discussion_id: str) -> None:
        pass

    @abstractmethod
    async def get_code_snippet_from_path(self, path: str) -> str:
        pass
