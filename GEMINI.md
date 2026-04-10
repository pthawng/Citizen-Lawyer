# Citizen Lawyer - Legal Assistant RAG System

## 1. Project Overview
**Product Vision:** A specialized AI legal assistant for Vietnamese civil law, providing accurate legal article extraction with clear citations and zero hallucinations via a grounded RAG (Retrieval-Augmented Generation) pipeline.

**Core Value:** Simplifies legal research by navigating complex, fragmented laws using an optimized RAG pipeline with reranking and metadata filtering.

## 2. Technical Stack
- **Orchestration:** LangGraph (Stateful, cyclic workflows)
- **Vector Store:** Qdrant (Cloud) / pgvector (On-premise)
- **Embeddings:** `intfloat/multilingual-e5-large` (1024d)
- **Reranker:** `BAAI/bge-reranker-base` (Cross-encoder)
- **LLMs:** 
  - Production: OpenAI GPT-4o
  - Local/Fallback: Qwen2.5-72B-Instruct (via vLLM)
  - Research/Gemini: Gemini 1.5 Pro
- **API:** FastAPI (Async, type-safe)
- **ETL/Data Pipeline:** Prefect, unstructured.io (PDF/Word parsing)
- **Monitoring:** Langfuse / Arize Phoenix (Observability, cost, latency)

## 3. Engineering Standards & Workflows

### 3.1 RAG Strategy & Reasoning
- **Chunking:** ALWAYS use **Article-Level Chunking**. Do not use fixed-size chunking as it breaks legal context and citation integrity.
- **Multi-step Query Decomposition:** Complex queries must be decomposed into sub-queries by a `QueryDecomposer` before retrieval.
- **Retrieval Abstraction:** All retrieval logic (Hybrid Search + Reranking) must be encapsulated in a `BaseRetriever` interface to ensure modularity and testability.

### 3.2 Hallucination Prevention & Conflict Resolution
- **Strict Grounding:** The system must only answer based on the provided `[CONTEXT]`.
- **Conflict Resolution (Lex Specialis):** If retrieved articles conflict, prioritize specialized laws over general laws and higher legal hierarchies.
- **Citation Enforcement:** Every response must include citations in the format `[Điều X, Luật Y, năm Z]`.
- **Thresholds:** If reranker confidence < 0.7, trigger a `LowConfidenceError`.

### 3.3 Dependency Injection & Configuration
- **Centralized Settings:** Use Pydantic `BaseSettings` for all environment variables (API keys, model names, DB URLs).
- **DI Pattern:** Use FastAPI's dependency injection or a simple `get_...` pattern to provide instances of `QdrantClient`, `ChatOpenAI`, and `BaseRetriever`.

### 3.4 Schema & DTO Enforcement
- **Internal Schema:** Articles must follow the `ArticleChunk` Pydantic model.
- **API DTOs:** Explicitly define `ChatRequest` and `ChatResponse` models to maintain a stable contract with the frontend.

### 3.5 Observability & Error Handling
- **Custom Exceptions:** Define RAG-specific exceptions (e.g., `NoContextFoundError`, `HallucinationDetectedError`) in `app/core/exceptions.py`.
- **Tracing:** Wrap all LLM and Retrieval calls with Langfuse tracers to monitor latency and cost.

## 4. Repository Structure & Core Modules
- `app/api/`: FastAPI routes and DTOs.
- `app/core/`: `settings.py`, `dependencies.py`, `exceptions.py`.
- `app/rag/`:
  - `query/`: `analyzer.py`, `decomposer.py`.
  - `retrieval/`: `base.py`, `hybrid_search.py`, `reranker.py`.
  - `generation/`: `generator.py`, `citations.py`.
- `app/prompts/`: Structured, versioned `.txt` or `.yaml` prompt templates.
- `app/services/`: `conversation_service.py` (State management).
- `app/data_pipeline/`: ETL, parsers, and chunkers.
- `eval/`: `dataset.json`, `evaluator.py`, `metrics.py`.
- `tests/`: Unit, integration, and RAG-specific "golden set" tests.

## 5. Deployment & Validation
- **Environments:** Dev, Staging, Prod with specific model fallbacks.
- **CI/CD:** Automated evaluation suite (Hit Rate@5, MRR) must pass before staging/prod deployment.

## 6. AI Interaction Directives
- **Code Style:** No boilerplate. Use Python 3.11+ features.
- **Implementation:** Always check `app/core/dependencies.py` before instantiating clients.
- **Prompting:** Use externalized prompt templates from `app/prompts/` instead of hardcoded strings.
- **Safety:** Refuse to hallucinate or bypass legal grounding (Section 3.2).

---
*Last Updated: April 2026 | Maintainer: Le Phuoc Thang*
