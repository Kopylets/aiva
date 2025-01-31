from abc import ABC, abstractmethod


class BaseProvider(ABC):
    @abstractmethod
    async def publish_code_suggestions(self, code_suggestions: list) -> bool:
        pass
