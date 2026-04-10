from app.rag.retriever import BaseRetriever
from app.rag.generator import BaseGenerator
from app.models.schemas import ChatResponse


class RAGPipeline:
    def __init__(self, retriever: BaseRetriever, generator: BaseGenerator):
        self.retriever = retriever
        self.generator = generator

    async def answer(self, query: str) -> ChatResponse:
        """
        Orchestrates the RAG flow:
        1. Retrieve relevant chunks
        2. Generate grounded response
        3. Extract and format citations
        """
        # TODO: Implement orchestration logic
        chunks = await self.retriever.retrieve(query)
        answer = await self.generator.generate(query, chunks)
        
        # Temporary mock of citation extraction
        citations = [
            f"[{c.metadata.article_id}, {c.metadata.law_name}, {c.metadata.year}]"
            for c in chunks
        ]
        
        return ChatResponse(answer=answer, citations=list(set(citations)))
