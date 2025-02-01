from abc import ABC, abstractmethod

from presentation.api_v1.providers.gitlab.schemas import CommentOnCodeSnippetEvent


class BaseCodeSuggestService(ABC):
    @abstractmethod
    async def suggest_code(self, comment_on_code_snippet: CommentOnCodeSnippetEvent) -> None:
        pass
