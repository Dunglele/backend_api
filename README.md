# Shop Backend API (FastAPI)

Dự án cung cấp các endpoint API cho Mobile App và Admin Dashboard.

# Shop Backend API (FastAPI)

Dự án cung cấp các endpoint API cho Mobile App và Admin Dashboard.

## 🚀 Hướng dẫn chạy

### 1. Chạy trên máy local
Để chạy API phục vụ cho việc phát triển trên cùng một máy:
1. Truy cập thư mục: `cd backend_api`
2. Chạy Server:
   ```powershell
   # Sử dụng python -m để tránh lỗi launcher nếu di chuyển thư mục env
   ..\env\Scripts\python.exe -m uvicorn app.main:app --reload
   ```
3. Truy cập: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 2. Chạy cho thiết bị di động (Matepad, Android, iOS)
Để thiết bị di động truy cập được API qua Wi-Fi hoặc Mobile Hotspot:
1. Chạy Server với host `0.0.0.0`:
   ```powershell
   ..\env\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0
   ```
2. Tìm IP của máy tính (dùng `ipconfig`). Ví dụ: `192.168.137.1`.
3. Cập nhật Base URL trong Mobile App thành: `http://<IP_CUA_BAN>:8000`

## 🔗 Link hữu ích
- **Tài liệu API (Swagger):** http://127.0.0.1:8000/docs
- **Admin Login:** Sử dụng tài liệu `admin_account.txt` ở thư mục gốc.

