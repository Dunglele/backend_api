from app.database import SessionLocal
from app import models

def cleanup_data():
    db = SessionLocal()
    try:
        print("Đang dọn dẹp dữ liệu thiếu thông tin...")
        
        # 1. Xóa sản phẩm có giá trị null ở các trường quan trọng
        deleted_products = db.query(models.Product).filter(
            (models.Product.image_url == None) | 
            (models.Product.size == None) | 
            (models.Product.color == None)
        ).delete(synchronize_session=False)
        
        # 2. Xóa danh mục thiếu ảnh
        deleted_categories = db.query(models.Category).filter(
            models.Category.image_url == None
        ).delete(synchronize_session=False)
        
        db.commit()
        print(f"--- DỌN DẸP HOÀN TẤT ---")
        print(f"- Đã xóa {deleted_products} sản phẩm không đầy đủ.")
        print(f"- Đã xóa {deleted_categories} danh mục không đầy đủ.")
        
    except Exception as e:
        print(f"Lỗi: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    cleanup_data()
