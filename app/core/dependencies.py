from functools import lru_cache
from app.rag.base import BaseRetriever, BaseGenerator
from app.rag.retriever import QdrantRetriever
from app.rag.generator import OpenAIGenerator
from app.rag.pipeline import RAGPipeline


@lru_cache
def get_retriever() -> BaseRetriever:
    """
    Initializes and returns a singleton instance of QdrantRetriever.
    """
    return QdrantRetriever()


@lru_cache
def get_generator() -> BaseGenerator:
    """
    Initializes and returns a singleton instance of OpenAIGenerator.
    """
    return OpenAIGenerator()


async def get_rag_pipeline() -> RAGPipeline:
    """
    Dependency for FastAPI endpoints to get the RAG Pipeline instance.
    """
    return RAGPipeline(
        retriever=get_retriever(),
        generator=get_generator()
    )
