# 🌏 TravelBuddy AI Agent - Modernization (Day 6 Hackathon)

Chào mừng bạn đến với phiên bản cải tiến của **TravelBuddy**, một trợ lý du lịch AI được xây dựng trên nền tảng **LangGraph 0.2** và **Next.js**. Dự án này đã được tối ưu hóa về hiệu năng, quản lý trạng thái và tích hợp hệ thống Telemetry chi tiết.

## 🚀 Tính năng nổi bật
- **LangGraph 0.2 Infrastructure**: Sử dụng StateGraph hiện đại để quản lý luồng suy nghĩ của AI.
- **Dynamic Location Injection**: Tự động nhận diện và đưa vị trí người dùng vào Prompt để phản hồi chính xác.
- **Smart Itinerary Actions**: Tự động trích xuất JSON để vẽ lộ trình du lịch trên bản đồ Frontend.
- **Telemetry System**: Theo dõi độ trễ (Latency) và số lượng Token tiêu thụ trong thời gian thực.
- **Clean UI/UX**: Giao diện hiện đại, hỗ trợ streaming và xử lý lỗi vòng lặp React.

---

## 🛠️ Hướng dẫn cài đặt và Khởi chạy

Dự án gồm 2 module chính: `backend` (FastAPI) và `frontend` (Next.js).

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

---

## 📊 Theo dõi AI (Telemetry)
Khi sử dụng ứng dụng, hãy quan sát Terminal của Backend để thấy các thông số hiệu năng:
- **🛠️ GỌI CÔNG CỤ**: Chi tiết các hàm AI đang thực thi.
- **⏱️ Độ trễ**: Thời gian AI phản hồi.
- **🎟️ Token**: Số lượng token tiêu thụ cho mỗi lượt chat.

---

## 🔗 Liên kết Repository
Dự án được lưu trữ tại: [https://github.com/7kitan/day6_hackathon_A3](https://github.com/7kitan/day6_hackathon_A3)

---
*Phát triển bởi Nguyen Bach - Hackathon AI Thực Chiến 2026.*
# day6_hackathon_A3
# day6_hackathon_A3
