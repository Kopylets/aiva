from abc import ABC, abstractmethod


class BaseCodeSuggestService(ABC):
    @abstractmethod
    async def suggest_code(self, comment: str) -> None:
        pass
