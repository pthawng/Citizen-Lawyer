from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.rag.base import BaseGenerator
from app.models.schemas import ArticleChunk
from app.core.settings import settings

class OpenAIGenerator(BaseGenerator):
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.LLM_MODEL,
            openai_api_key=settings.OPENAI_API_KEY,
            temperature=0
        )
        
        self.system_prompt = """
Bạn là trợ lý pháp lý chuyên nghiệp về luật Việt Nam. 
Nhiệm vụ của bạn là trả lời câu hỏi của người dùng dựa TRÊN DUY NHẤT ngữ cảnh pháp luật được cung cấp dưới đây.

[CONTEXT]
{context}

QUY TẮC NGHIÊM NGẶT:
1. Chỉ trả lời dựa trên thông tin trong [CONTEXT]. Nếu không có thông tin, hãy nói "Tôi không tìm thấy thông tin trong các văn bản pháp luật hiện hành."
2. Mọi câu trả lời PHẢI kèm trích dẫn ở cuối câu hoặc đoạn văn theo định dạng: [Điều X, Luật Y, năm Z].
3. Nếu các điều luật mâu thuẫn, hãy ưu tiên luật chuyên ngành hoặc văn bản có hiệu lực cao hơn.
4. Trả lời bằng tiếng Việt, phong cách chuyên nghiệp, chính xác.
"""

    async def generate(self, query: str, context: list[ArticleChunk]) -> str:
        """
        Generates a grounded response using OpenAI GPT model.
        """
        if not context:
            return "Tôi không tìm thấy thông tin trong các văn bản pháp luật hiện hành."

        # Format context for the prompt
        context_text = "\n\n".join([
            f"--- {c.metadata.law_name} ({c.metadata.year}) ---\n{c.content}"
            for c in context
        ])

        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "{query}")
        ])

        chain = prompt | self.llm
        
        response = await chain.ainvoke({
            "context": context_text,
            "query": query
        })
        
        return response.content
