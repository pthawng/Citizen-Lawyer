import requests
import json

def test_chat():
    url = "http://127.0.0.1:8000/api/v1/chat/"
    
    # Câu hỏi mẫu dựa trên Bộ luật Dân sự Điều 1, 2, 3
    query = "Các nguyên tắc cơ bản của pháp luật dân sự Việt Nam là gì?"
    
    payload = {
        "query": query,
        "session_id": "test_session_001"
    }
    
    print(f"SENDER: {query}")
    print("-" * 30)
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        print(f"ASSISTANT: {result['answer']}")
        print(f"\nCITATIONS: {result['citations']}")
        
    except Exception as e:
        print(f"Lỗi khi gọi API: {e}")
        print("Đảm bảo bạn đã chạy uvicorn trước khi chạy script này.")

if __name__ == "__main__":
    test_chat()
