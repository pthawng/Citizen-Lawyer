from abc import ABC, abstractmethod
from app.models.schemas import ArticleChunk


class BaseRetriever(ABC):
    @abstractmethod
    async def retrieve(self, query: str, limit: int = 5) -> list[ArticleChunk]:
        """
        Execute hybrid search followed by reranking.
        Must respect temporal filters and legal hierarchy.
        """
        pass
