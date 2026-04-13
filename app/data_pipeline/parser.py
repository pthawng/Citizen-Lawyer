import re
from typing import List
from app.models.schemas import ArticleChunk, ArticleMetadata

class LegalParser:
    def __init__(self, law_name: str, year: int):
        self.law_name = law_name
        self.year = year

    def parse_markdown(self, text: str) -> List[ArticleChunk]:
        """
        Parses legal text in markdown format and splits it into ArticleChunks.
        Expected format: 'Điều X. Tên điều\nNội dung...'
        """
        # Split by 'Điều X.'
        # Use Lookahead to keep the 'Điều' prefix
        pattern = r'(?=Điều \d+[\.:]?)'
        sections = re.split(pattern, text)
        
        chunks = []
        for section in sections:
            section = section.strip()
            if not section.startswith("Điều"):
                continue  # Skip preamble or headers before the first article
                
            # Extract Article ID (e.g., 'Điều 1')
            lines = section.split('\n')
            article_header = lines[0]
            article_id_match = re.search(r'Điều (\d+)', article_header)
            
            if article_id_match:
                article_id = f"Điều {article_id_match.group(1)}"
                
                metadata = ArticleMetadata(
                    article_id=article_id,
                    law_name=self.law_name,
                    year=self.year,
                    legal_hierarchy=1  # Default for main laws
                )
                
                chunk = ArticleChunk(
                    content=section,
                    metadata=metadata
                )
                chunks.append(chunk)
                
        return chunks
