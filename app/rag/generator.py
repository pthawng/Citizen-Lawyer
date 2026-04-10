from abc import ABC, abstractmethod
from app.models.schemas import ArticleChunk


class BaseGenerator(ABC):
    @abstractmethod
    async def generate(self, query: str, context: list[ArticleChunk]) -> str:
        """
        Generate a grounded response based ONLY on context.
        Must enforce citation format: [Điều X, Luật Y, năm Z].
        """
        pass
