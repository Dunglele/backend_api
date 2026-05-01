from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import admin, client

# Tạo bảng trong CSDL
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Shop API Backend",
    description="Backend API cho hệ thống Mobile App và Admin Dashboard",
    version="2.0.0"
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Cho phép tất cả các nguồn trong giai đoạn phát triển
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(admin.router)
app.include_router(client.router)

@app.get("/")
def read_root():
    return {"message": "Chào mừng bạn đến với Shop API Backend!"}
