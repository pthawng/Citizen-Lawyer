from qdrant_client import AsyncQdrantClient
from sentence_transformers import SentenceTransformer
from app.rag.base import BaseRetriever
from app.models.schemas import ArticleChunk, ArticleMetadata
from app.core.settings import settings

class QdrantRetriever(BaseRetriever):
    def __init__(self):
        # Sử dụng AsyncQdrantClient cho hiệu năng tốt hơn trong FastAPI
        self.client = AsyncQdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)
        self.collection_name = settings.COLLECTION_NAME

    async def retrieve(self, query: str, limit: int = 5) -> list[ArticleChunk]:
        """
        Truy xuất các điều luật liên quan từ Qdrant sử dụng Async search.
        """
        # E5 model: thêm tiền tố 'query: ' để tìm kiếm đạt độ chính xác cao nhất
        query_vector = self.model.encode(f"query: {query}").tolist()
        
        # Sử dụng API query_points (hiện đại hơn search)
        search_result = await self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
            with_payload=True
        )
        
        chunks = []
        for point in search_result.points:
            metadata_dict = point.payload.get("metadata", {})
            metadata = ArticleMetadata(**metadata_dict)
            
            chunk = ArticleChunk(
                content=point.payload.get("content", ""),
                metadata=metadata,
                score=point.score
            )
            chunks.append(chunk)
            
        return chunks
