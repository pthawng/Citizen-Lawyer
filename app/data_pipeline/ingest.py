import os
import asyncio
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
from app.core.settings import settings
from app.data_pipeline.parser import LegalParser

async def ingest_sample_data():
    print("Starting ingestion process...")
    
    # 1. Load Data
    data_path = "data/sample/civil_law_sample.md"
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        text = f.read()

    # 2. Parse Data
    parser = LegalParser(law_name="Bộ luật Dân sự", year=2015)
    chunks = parser.parse_markdown(text)
    print(f"Parsed {len(chunks)} articles.")

    # 3. Initialize Embedding Model
    print(f"Loading embedding model: {settings.EMBEDDING_MODEL}...")
    # Note: multilingual-e5-large requires 'query: ' or 'passage: ' prefix for best results
    model = SentenceTransformer(settings.EMBEDDING_MODEL)

    # 4. Initialize Qdrant
    print(f"Connecting to Qdrant at {settings.QDRANT_URL}...")
    client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)

    # Create collection if not exists
    vector_size = 1024  # Size for multilingual-e5-large
    collections = client.get_collections().collections
    exists = any(c.name == settings.COLLECTION_NAME for c in collections)

    if not exists:
        print(f"Creating collection: {settings.COLLECTION_NAME}")
        client.create_collection(
            collection_name=settings.COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=vector_size, 
                distance=models.Distance.COSINE
            )
        )

    # 5. Embed and Upsert
    print("Generating embeddings and upserting...")
    points = []
    for i, chunk in enumerate(chunks):
        # E5 model trick: prefix with 'passage: ' for indexing
        embedding = model.encode(f"passage: {chunk.content}").tolist()
        
        points.append(
            models.PointStruct(
                id=i,
                vector=embedding,
                payload={
                    "content": chunk.content,
                    "metadata": chunk.metadata.model_dump()
                }
            )
        )

    client.upsert(
        collection_name=settings.COLLECTION_NAME,
        points=points
    )
    print(f"Successfully ingested {len(points)} points into Qdrant.")

if __name__ == "__main__":
    asyncio.run(ingest_sample_data())
