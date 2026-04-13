# Citizen Lawyer - Trợ Lý Pháp Luật RAG

Hệ thống trợ lý AI chuyên biệt cho Luật dân sự Việt Nam, giúp trích xuất các điều luật chính xác với trích dẫn rõ ràng, đảm bảo không ảo giác thông qua quy trình RAG (Retrieval-Augmented Generation).

## 🚀 Tính năng cốt lõi (Giai đoạn 1)

- **Chống ảo giác:** Câu trả lời dựa hoàn toàn vào ngữ cảnh pháp lý được truy xuất.
- **Trích dẫn bắt buộc:** Mọi câu trả lời đều kèm theo nguồn theo định dạng `[Điều X, Luật Y, năm Z]`.
- **Truy xuất nâng cao:** Tìm kiếm Vector bất đồng bộ với Qdrant và mô hình `multilingual-e5-large`.
- **Phân tách theo Điều luật:** Đảm bảo toàn vẹn ngữ cảnh pháp lý thông qua bài toán chunking theo Article-level.

## 🛠 Công nghệ sử dụng

- **Backend:** FastAPI
- **Vector Database:** Qdrant (Docker)
- **Mô hình ngôn ngữ (LLM):** OpenAI GPT-4o-mini
- **Embeddings:** `intfloat/multilingual-e5-large` (Chạy cục bộ)

## 📁 Cấu trúc thư mục

```text
app/
├── api/          # Tuyến đường FastAPI và DTOs
├── core/         # Cấu hình, phụ thuộc và ngoại lệ
├── models/       # Pydantic schemas và domain models
├── rag/          # Logic RAG (Retriever, Generator, Pipeline)
├── data_pipeline/# ETL (Bộ tách, Bộ nạp dữ liệu)
└── main.py       # Điểm khởi chạy ứng dụng
```

## ⚙️ Hướng dẫn cài đặt nhanh (Windows)

1. **Khởi chạy Qdrant Server:**
   ```powershell
   docker run -p 6333:6333 qdrant/qdrant
   ```

2. **Cấu hình môi trường:**
   Tạo file `.env` từ `.env.example` và điền `OPENAI_API_KEY` của bạn.

3. **Nạp dữ liệu pháp luật:**
   ```powershell
   py -m app.data_pipeline.ingest
   ```

4. **Chạy Server API:**
   ```powershell
   py -m uvicorn app.main:app --reload
   ```

5. **Chạy thử nghiệm truy vấn:**
   ```powershell
   py test_rag.py
   ```

---
*Trạng thái: Giai đoạn 1 (Hạ tầng RAG lõi) - HOÀN THÀNH.*
