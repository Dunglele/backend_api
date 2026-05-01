from app.database import SessionLocal
from app import models, auth
import sys

def create_admin(email, password, full_name):
    db = SessionLocal()
    try:
        db_user = db.query(models.User).filter(models.User.email == email).first()
        if db_user:
            print(f"Lỗi: Email {email} đã tồn tại.")
            return

        hashed_password = auth.get_password_hash(password)
        admin_user = models.User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            role="admin"
        )
        db.add(admin_user)
        db.commit()
        print(f"Thành công: Đã tạo tài khoản Admin cho {email}")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Sử dụng: python create_admin.py <email> <password> <full_name>")
    else:
        create_admin(sys.argv[1], sys.argv[2], sys.argv[3])
