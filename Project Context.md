# Citizen Lawyer - Legal Assistant RAG System

## 1. Executive Summary

**Product Vision:** Một trợ lý pháp lý AI chuyên sâu cho lĩnh vực luật dân sự Việt Nam, có khả năng trích xuất chính xác điều khoản từ văn bản quy phạm pháp luật, kèm citation rõ ràng, loại bỏ hoàn toàn hallucination bằng cơ chế grounded generation.

**Value Proposition:** Giải quyết vấn đề tra cứu pháp lý phức tạp, nơi người dùng phải đọc hàng nghìn điều luật phân tán trong nhiều văn bản khác nhau. Hệ thống đảm bảo độ chính xác tuyệt đối về mặt pháp lý thông qua RAG pipeline được tối ưu với reranking và metadata filtering.

**Current Status:** Production-ready MVP với kiến trúc modular, hỗ trợ deployment trên cloud (AWS/GCP) hoặc on-premise với GPU.

---

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ Streamlit│  │  Chainlit│  │ REST API │  │  Webhook │       │
│  │   UI     │  │  Chat    │  │ FastAPI  │  │ (Slack)  │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
└─────────────────────────────┬───────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                      ORCHESTRATION LAYER                        │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              LangGraph / LangChain Agent                  │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │  │
│  │  │ Query Router│  │Retrieval Node│  │Generation   │      │  │
│  │  │(Intent Class)│  │(Multi-Query)│  │ Node        │      │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘      │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────┬───────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                      RETRIEVAL LAYER                            │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Vector Store: Qdrant / Pinecone                        │   │
│  │  ┌────────────────────────────────────────────────────┐  │   │
│  │  │ Collections:                                       │  │   │
│  │  │ • legal_documents (main)                          │  │   │
│  │  │   - embedding: multilingual-e5-large (1024d)      │  │   │
│  │  │   - metadata: law_name, article_id, effective_date│  │   │
│  │  └────────────────────────────────────────────────────┘  │   │
│  │                                                          │   │
│  │  ┌────────────────────────────────────────────────────┐  │   │
│  │  │ Reranker: BAAI/bge-reranker-base (cross-encoder)  │  │   │
│  │  └────────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────┬───────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                      GENERATION LAYER                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  LLM Gateway (Unified Interface)                        │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐       │   │
│  │  │ OpenAI GPT-│  │ Gemini    │  │ Qwen2.5-72B│       │   │
│  │  │ 4o (Prod)  │  │ 1.5 Pro   │  │ (Local)    │       │   │
│  │  └────────────┘  └────────────┘  └────────────┘       │   │
│  │                                                          │   │
│  │  Prompt Template: Structured with citation enforcement │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────┬───────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                      DATA PIPELINE LAYER                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  ETL Pipeline (Prefect / Airflow)                       │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐       │   │
│  │  │ PDF/Word  │→ │ Structure  │→ │ Chunking   │       │   │
│  │  │ Crawler   │  │ Parser     │  │ by Article │       │   │
│  │  └────────────┘  └────────────┘  └────────────┘       │   │
│  │                              ↓                           │   │
│  │                    ┌────────────────────┐               │   │
│  │                    │ Embedding & Index  │               │   │
│  │                    └────────────────────┘               │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Technology Stack

| Layer | Technology | Rationale |
|---|---|---|
| Orchestration | LangGraph | Stateful, cyclic workflows; better than LangChain for complex RAG with reflection loops |
| Vector Store | Qdrant (cloud) / pgvector (self-hosted) | Qdrant: best filtering performance; pgvector: if compliance requires on-prem |
| Embeddings | intfloat/multilingual-e5-large | Top MIRACL benchmark for Vietnamese; 1024-dim balances accuracy & cost |
| Reranker | BAAI/bge-reranker-base | Cross-encoder improves recall@5 by 15-20% vs vector-only |
| LLM (Prod) | OpenAI GPT-4o | Vietnamese fluency, function calling, 128k context for full article display |
| LLM (Local) | Qwen2.5-72B-Instruct | Open-weight, SOTA Vietnamese performance, deployable via vLLM |
| ETL | Prefect | Lightweight, Python-native, easier than Airflow for data pipeline |
| Parsing | unstructured.io + custom | Handles complex legal PDF structure (tables, nested articles) |
| API | FastAPI | Async, auto-docs, type hints, easy middleware for auth/logging |
| Monitoring | Langfuse / Arize Phoenix | LLM observability: trace costs, latency, hallucination score |

---

## 3. Core Technical Decisions & Rationale

### 3.1 Why Article-Level Chunking (not Fixed-Size)?

**Problem:** Legal documents have hierarchical structure (Điều → Khoản → Điểm). Fixed-size chunking (e.g., 512 tokens) breaks article boundaries, causing:
- Incomplete legal context
- Citation loss (can't pinpoint exact article number)

**Solution:**

```python
# Custom parser preserves legal structure
class LegalDocumentParser:
    def parse(self, text: str) -> List[Article]:
        # Regex pattern for "Điều [0-9]+[\.]?.*"
        # Each Article becomes one chunk with metadata:
        # - article_id: "Điều 10"
        # - law_name: "Luật Hôn nhân Gia đình 2014"
        # - effective_date: "2015-01-01"
        # - clauses: list of sub-articles for granular retrieval
```

### 3.2 Multi-Stage Retrieval Strategy

Single-stage retrieval is insufficient for legal queries where precision is critical.

**Our 3-stage pipeline:**

| Stage | Method | Purpose |
|---|---|---|
| 1. Hybrid Search | Vector (0.7) + BM25 (0.3) | Recall: captures semantic + keyword matches (legal terms often exact) |
| 2. Reranking | Cross-encoder (bge-reranker) | Precision: reorders top-20 to top-5 by relevance |
| 3. Metadata Filtering | Time-aware filter | Accuracy: only return articles effective at query time |

### 3.3 Hallucination Mitigation

Strict prompt engineering + guardrails:

```python
SYSTEM_PROMPT = """
Bạn là trợ lý pháp lý. QUAN TRỌNG:
1. CHỈ trả lời dựa trên [CONTEXT] được cung cấp.
2. Nếu câu hỏi không liên quan đến pháp luật, từ chối lịch sự.
3. Nếu [CONTEXT] không đủ thông tin, nói "Tôi không tìm thấy thông tin trong văn bản pháp luật hiện hành."
4. MỖI câu trả lời phải kèm trích dẫn [Điều X, Luật Y, năm Z] ở cuối.
5. KHÔNG suy diễn, KHÔNG thêm thông tin ngoài [CONTEXT].
"""
```

**Additional guardrails:**
- **Citation validation:** Generated citation must exist in retrieved chunks (post-hoc verification)
- **Confidence threshold:** If reranker score < 0.7, force "uncertain" response

### 3.4 Temporal Awareness

**Challenge:** Laws change over time. A query about "lương tối thiểu" in 2025 vs 2023 yields different answers.

**Solution:** Metadata filtering with `effective_date` range.

```python
def retrieve_with_time_filter(query: str, query_date: date):
    return vector_store.search(
        query,
        filter={
            "must": [
                {"key": "effective_date", "range": {"lte": query_date}},
                {"key": "expiry_date", "range": {"gte": query_date}}
            ]
        }
    )
```

---

## 4. Data Pipeline & ETL

### 4.1 Data Sources

| Source | Format | Volume | Update Frequency |
|---|---|---|---|
| Cổng VBPL (vbpq) | HTML | 500+ laws | Monthly |
| Thư viện pháp luật | PDF | 2000+ docs | Quarterly |
| Official Gazette | PDF | 50-100 new/month | Weekly |

### 4.2 Pipeline Architecture

```
[Raw Data] → [Parser] → [Structure Extractor] → [Chunker] → [Embedding] → [Index]

Prefect Flow:
├── task: download_from_sources()
├── task: convert_to_markdown()  # unstructured.io
├── task: extract_legal_structure()  # custom regex + AST
├── task: chunk_by_article()  # preserve hierarchy
├── task: generate_embeddings()  # batch inference
├── task: upsert_to_qdrant()  # idempotent
└── task: update_metadata_registry()  # version tracking
```

### 4.3 Idempotency & Incremental Updates

- Each document has `version_id` (hash of content + metadata)
- Upsert operation: if `version_id` exists, skip or update
- Support for document expiration: soft-delete via `is_active` flag

---

## 5. API Design

### 5.1 REST Endpoints

```yaml
POST /api/v1/chat
  Request:
    {
      "message": "string",
      "conversation_id": "uuid | null",
      "filters": {
        "effective_date": "2025-01-01 | null",
        "law_names": ["string"] | null
      }
    }
  
  Response:
    {
      "response": "string",
      "citations": [
        {
          "article": "Điều 10",
          "law": "Luật Hôn nhân Gia đình 2014",
          "text_preview": "string",
          "full_text_url": "/api/v1/articles/{id}"
        }
      ],
      "conversation_id": "uuid",
      "confidence_score": 0.92
    }

POST /api/v1/feedback
  Request: { "conversation_id": "uuid", "rating": 1|0, "comment": "string" }
```

### 5.2 Async Support

- Long-running queries (>5s) return `202 Accepted` with `task_id`
- Webhook callback or polling via `GET /api/v1/tasks/{task_id}`

---

## 6. Evaluation & Observability

### 6.1 Offline Evaluation Metrics

| Metric | Target | Method |
|---|---|---|
| Hit Rate@5 | >0.85 | % queries where correct article in top-5 retrieved |
| MRR | >0.80 | Mean Reciprocal Rank of correct article |
| Citation Accuracy | 100% | % responses where citations are valid |
| Hallucination Rate | <2% | Human eval / LLM-as-judge (GPT-4) |
| End-to-End Latency | <3s p95 | Production SLA |

### 6.2 Online Monitoring (Langfuse)

- Trace per request: embedding latency, retrieval latency, LLM latency, token usage
- User feedback loop: collect 👍/👎 to build golden dataset
- Cost tracking: $ per conversation, per model

### 6.3 A/B Testing Framework

- Model comparison: GPT-4o vs Gemini 1.5 Pro vs Qwen2.5
- Chunking strategy: article-level vs fixed-size
- Retrieval strategy: vector-only vs hybrid+reranker

---

## 7. Deployment Strategy

### 7.1 Environment Matrix

| Environment | LLM | Vector DB | Purpose |
|---|---|---|---|
| Dev | GPT-4o-mini | Qdrant (cloud free) | Local development, CI tests |
| Staging | GPT-4o | Qdrant (dedicated) | Integration tests, load testing |
| Prod | GPT-4o + Qwen2.5 fallback | Qdrant (replicated) | Production traffic, high availability |

### 7.2 Infrastructure (Terraform managed)

```hcl
# AWS / GCP
- EKS / GKE: orchestration
- GPU nodes (A10G): for local LLM (optional)
- RDS PostgreSQL: conversation history, feedback
- S3/GCS: raw PDF storage
- CloudFront/CDN: static assets
```

### 7.3 CI/CD Pipeline

```
PR → Tests (unit + integration) → Build Docker image → Deploy to staging →
  Run evaluation suite (100 queries) → If pass → Deploy to prod (blue/green)
```

---

## 8. Future Roadmap

| Phase | Feature | Priority |
|---|---|---|
| Q3 2026 | Agentic RAG: multi-hop reasoning for cross-law queries | High |
| Q4 2026 | Speech-to-text + Vietnamese voice interface | Medium |
| Q1 2027 | Document upload: users upload contracts, get clause-by-clause analysis | High |
| Q2 2027 | Fine-tuned embedding model on legal Vietnamese corpus | Medium |
| Ongoing | Expand to criminal law, commercial law domains | Medium |

---

## 9. Getting Started (for Contributors)

### Prerequisites

- Python 3.11+
- Docker + Docker Compose
- OpenAI API key (or local GPU with 24GB+ VRAM for Qwen2.5-72B)

### Quick Start

```bash
# Clone repository
git clone https://github.com/[your-repo]/citizen-lawyer.git
cd citizen-lawyer

# Setup environment
cp .env.example .env
# Add your API keys

# Run with Docker
docker-compose up -d

# Index sample legal documents
python scripts/ingest.py --source data/sample/

# Start development server
uvicorn app.main:app --reload
```

### Repository Structure

```
citizen-lawyer/
├── app/
│   ├── api/           # FastAPI endpoints
│   ├── core/          # Config, dependencies
│   ├── models/        # Pydantic schemas
│   ├── rag/           # RAG pipeline: retrieval, generation
│   │   ├── retriever.py
│   │   ├── reranker.py
│   │   └── generator.py
│   ├── data_pipeline/ # ETL: parsers, chunkers
│   └── utils/         # Helpers, logging
├── scripts/           # Ingestion, evaluation, maintenance
├── tests/             # Unit + integration tests
├── deployments/       # Kubernetes manifests, Terraform
└── docs/              # Architecture diagrams, API docs
```

---

## 10. Team & Roles

| Role | Responsibilities |
|---|---|
| AI Engineer (pthawngs) | RAG pipeline design, evaluation, prompt engineering, production deployment |
| ML Engineer | Embedding fine-tuning, vector DB optimization |
| Backend Engineer | API development, ETL pipeline, infrastructure |
| Legal Domain Expert | Golden dataset annotation, validation |

---

*Last Updated: April 2026 | Maintainer: [Le Phuoc Thang]*
