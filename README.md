# (XanhSM) Holiday Mode AI Agent (Day 6 Hackathon)

Hỗ trợ user đặt tuyến đi xe du lịch local, cùng với recommendation các địa điểm tham quan và auto đặt xe

### Level: Demo Application (screenshot dưới đây)

## Phân Công

|Tên | Phần |
|-----|----|
| Kiệt | Implementation Plan + v2 Frontend fix UI + System Prompt + Test User Path |
| Bách | Backend (Routing) |
| Hoàng | v1 Frontend (Web version - đã bỏ) |
| Duy | Spec + Agent Tools |
| Giang | System Prompt + Agent Tools |
| Hưng | MapView API |

## Run Project
### 1. Backend (FastAPI)
Yêu cầu: Python 3.10+

1.  **Di chuyển vào thư mục backend**:
    ```bash
    cd backend
    ```
2.  **Tạo môi trường ảo và kích hoạt**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Trên Windows dùng: venv\Scripts\activate
    ```
3.  **Cài đặt các thư viện**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Cấu hình biến môi trường**:
    Tạo file `.env` và thêm key của bạn:
    ```env
    OPENAI_API_KEY=your_openai_api_key_here
    ```
5.  **Chạy Server**:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```

### 2. Frontend (Next.js)
Yêu cầu: Node.js 18+

1.  **Di chuyển vào thư mục frontend**:
    ```bash
    cd frontend
    ```
2.  **Cài đặt thư viện**:
    ```bash
    npm install
    ```
3.  **Cấu hình biến môi trường**:
    Tạo file `.env.local` nếu cần cấu hình API URL (mặc định là http://localhost:8000).
4.  **Chạy ứng dụng**:
    ```bash
    npm run dev
    ```

## Tools
- UI: v0 (Vercel)
- AI: Google Gemini 3.0 Flash 

## Liên kết Repository
Dự án được lưu trữ tại: [https://github.com/7kitan/day6_hackathon_A3](https://github.com/7kitan/day6_hackathon_A3)



