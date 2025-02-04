from abc import ABC, abstractmethod

from presentation.api_v1.providers.gitlab.schemas import CommentOnMergeRequestEvent


class BaseCodeSuggestService(ABC):
    @abstractmethod
    async def suggest_code(self, comment_on_mr_code_snippet: CommentOnMergeRequestEvent) -> None:
        pass
