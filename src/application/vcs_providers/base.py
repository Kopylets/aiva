from abc import ABC, abstractmethod
from typing import Optional


class BaseProvider(ABC):
    @abstractmethod
    async def publish_code_suggestion(self, code_suggestion: str, project_path: str, discussion_id: str,
                                      mr_id: int) -> None:
        pass

    @abstractmethod
    async def get_code_snippet_from_path(self, project_path: str, file_path: str, mr_id: int, start_line: Optional[int] = None, end_line: Optional[int] = None) -> str:
        pass
