# Citizen Lawyer - Legal Assistant RAG System

A specialized AI legal assistant for Vietnamese civil law, providing accurate legal article extraction with clear citations and zero hallucinations via a grounded RAG (Retrieval-Augmented Generation) pipeline.

## 🚀 Core Features

- **Zero Hallucination:** Answers are strictly grounded in retrieved legal contexts.
- **Mandatory Citation:** Every response includes citations in the format `[Điều X, Luật Y, năm Z]`.
- **Temporal Correctness:** Filtering based on `effective_date` and `expiry_date`.
- **Conflict Resolution:** Implements *Lex Specialis* and legal hierarchy logic.
- **Advanced Retrieval:** Hybrid search (Vector + BM25) combined with cross-encoder reranking.

## 🛠 Tech Stack

- **Orchestration:** LangGraph / Custom Async Pipeline
- **API Framework:** FastAPI (Python 3.11+)
- **Vector Store:** Qdrant
- **LLM:** OpenAI GPT-4o
- **Embeddings:** `intfloat/multilingual-e5-large`
- **Reranker:** `BAAI/bge-reranker-base`

## 📁 Project Structure

```text
app/
├── api/          # FastAPI routes and DTOs
├── core/         # Configuration, dependencies, and exceptions
├── models/       # Pydantic schemas and domain models
├── prompts/      # Externalized prompt templates
├── rag/          # RAG logic (Retriever, Generator, Pipeline)
├── services/     # Business logic and state management
└── main.py       # Application entry point
```

## ⚙️ Setup

1. **Environment Variables:**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_openai_key
   QDRANT_URL=http://localhost:6333
   QDRANT_API_KEY=your_qdrant_key
   ```

2. **Installation:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the API:**
   ```bash
   uvicorn app.main:app --reload
   ```

## 📜 Engineering Standards

This project follows strict engineering discipline:
- **Async-first design** for high-concurrency performance.
- **Type-safe** implementation using Pydantic and Python type hints.
- **Surgical updates:** Adherence to established architectural patterns and style.
- **Validation:** Every change is verified against the "golden set" of legal queries.

---
*Status: Development - Step 1 (Project Skeleton) Completed.*
