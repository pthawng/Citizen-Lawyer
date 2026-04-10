from functools import lru_cache
from app.rag.retriever import BaseRetriever
from app.rag.generator import BaseGenerator
from app.rag.pipeline import RAGPipeline


@lru_cache
def get_retriever() -> BaseRetriever:
    # TODO: Initialize QdrantRetriever with settings
    raise NotImplementedError("Retriever implementation pending")


@lru_cache
def get_generator() -> BaseGenerator:
    # TODO: Initialize OpenAIGenerator with settings
    raise NotImplementedError("Generator implementation pending")


async def get_rag_pipeline() -> RAGPipeline:
    return RAGPipeline(
        retriever=get_retriever(),
        generator=get_generator()
    )
