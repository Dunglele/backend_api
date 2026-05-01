import random
from app.database import SessionLocal, engine, Base
from app import models, auth

def seed_data():
    print("Khởi tạo cấu trúc bảng...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Tạo 5 người dùng ngẫu nhiên (bao gồm 1 admin đã có và 4 user mới)
        print("Đang tạo người dùng...")
        users_data = [
            ("hoang.nam@example.com", "Nam Hoàng", "user"),
            ("minh.anh@example.com", "Minh Anh", "user"),
            ("thu.thuy@example.com", "Thu Thủy", "user"),
            ("khanh.huyen@example.com", "Khánh Huyền", "user"),
        ]
        
        for email, name, role in users_data:
            if not db.query(models.User).filter(models.User.email == email).first():
                db.add(models.User(
                    email=email,
                    hashed_password=auth.get_password_hash("password123"),
                    full_name=name,
                    role=role
                ))

        # 2. Tạo Danh mục
        print("Đang tạo danh mục...")
        categories_data = [
            ("Áo Thun", "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500"),
            ("Sơ Mi", "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=500"),
            ("Quần Jeans", "https://images.unsplash.com/photo-1542272604-787c3835535d?w=500"),
            ("Váy & Đầm", "https://images.unsplash.com/photo-1539008835279-434674508233?w=500"),
            ("Phụ Kiện", "https://images.unsplash.com/photo-1523206489230-c012c64b2b48?w=500"),
        ]
        
        category_objects = []
        for name, img in categories_data:
            cat = db.query(models.Category).filter(models.Category.name == name).first()
            if not cat:
                cat = models.Category(name=name, image_url=img)
                db.add(cat)
                db.flush() # Để lấy ID ngay lập tức
            category_objects.append(cat)

        # 3. Tạo 30 sản phẩm
        print("Đang tạo 30 sản phẩm thời trang...")
        # Danh sách các bộ dữ liệu mẫu cho từng loại
        products_pool = [
            # Áo Thun (Category ID 0)
            {"name": "Áo Thun Oversize Streetwear", "price": 190000, "img": "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=800", "cat_idx": 0},
            {"name": "Áo Thun Trơn Basic", "price": 120000, "img": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=800", "cat_idx": 0},
            {"name": "Áo Thun Graphic Vintage", "price": 250000, "img": "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=800", "cat_idx": 0},
            {"name": "Áo Polo Nam Thanh Lịch", "price": 320000, "img": "https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=800", "cat_idx": 0},
            {"name": "Áo Thun Local Brand", "price": 350000, "img": "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=800", "cat_idx": 0},
            {"name": "Áo Thun Unisex Form Rộng", "price": 180000, "img": "https://images.unsplash.com/photo-1554568218-0f1715e72254?w=800", "cat_idx": 0},
            
            # Sơ Mi (Category ID 1)
            {"name": "Sơ Mi Trắng Công Sở", "price": 450000, "img": "https://images.unsplash.com/photo-1598033129183-c4f50c717658?w=800", "cat_idx": 1},
            {"name": "Sơ Mi Flanel Caro", "price": 380000, "img": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=800", "cat_idx": 1},
            {"name": "Sơ Mi Oxford Blue", "price": 420000, "img": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=800", "cat_idx": 1},
            {"name": "Sơ Mi Lụa Họa Tiết", "price": 550000, "img": "https://images.unsplash.com/photo-1594932224828-b4b05a83296c?w=800", "cat_idx": 1},
            {"name": "Sơ Mi Đen Slimfit", "price": 390000, "img": "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=800", "cat_idx": 1},
            {"name": "Sơ Mi Cổ Tàu Hiện Đại", "price": 410000, "img": "https://images.unsplash.com/photo-1621335829175-95f437384d7c?w=800", "cat_idx": 1},
            
            # Quần Jeans (Category ID 2)
            {"name": "Quần Jeans Slimfit Xanh Sáng", "price": 650000, "img": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=800", "cat_idx": 2},
            {"name": "Quần Jeans Baggy Đen", "price": 590000, "img": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=800", "cat_idx": 2},
            {"name": "Quần Short Jeans Mùa Hè", "price": 350000, "img": "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?w=800", "cat_idx": 2},
            {"name": "Jeans Rách Gối Cá Tính", "price": 720000, "img": "https://images.unsplash.com/photo-1604176354204-926873ff3da9?w=800", "cat_idx": 2},
            {"name": "Jeans Ống Suông Retro", "price": 680000, "img": "https://images.unsplash.com/photo-1602266272793-27d425313936?w=800", "cat_idx": 2},
            {"name": "Quần Kaki Chino", "price": 480000, "img": "https://images.unsplash.com/photo-1473966968600-fa804b86d30b?w=800", "cat_idx": 2},
            
            # Váy & Đầm (Category ID 3)
            {"name": "Đầm Hoa Nhí Dáng Dài", "price": 850000, "img": "https://images.unsplash.com/photo-1572804013307-59a8ffad517d?w=800", "cat_idx": 3},
            {"name": "Váy Suông Minimalist", "price": 520000, "img": "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=800", "cat_idx": 3},
            {"name": "Chân Váy Xếp Ly", "price": 350000, "img": "https://images.unsplash.com/photo-1582142306909-195724d33ffc?w=800", "cat_idx": 3},
            {"name": "Đầm Dự Tiệc Sang Trọng", "price": 1200000, "img": "https://images.unsplash.com/photo-1539008835279-434674508233?w=800", "cat_idx": 3},
            {"name": "Váy Bodycon Quyến Rũ", "price": 690000, "img": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=800", "cat_idx": 3},
            {"name": "Đầm Hai Dây Mùa Hè", "price": 450000, "img": "https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=800", "cat_idx": 3},
            
            # Phụ Kiện (Category ID 4)
            {"name": "Mũ Lưỡi Trai Streetwear", "price": 150000, "img": "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=800", "cat_idx": 4},
            {"name": "Thắt Lưng Da Cao Cấp", "price": 450000, "img": "https://images.unsplash.com/photo-1624222247344-550fb8ecf7c2?w=800", "cat_idx": 4},
            {"name": "Túi Tote Canvas", "price": 95000, "img": "https://images.unsplash.com/photo-1544816153-159c77bc15c4?w=800", "cat_idx": 4},
            {"name": "Kính Mát Thời Trang", "price": 280000, "img": "https://images.unsplash.com/photo-1511499767390-91f99f73948c?w=800", "cat_idx": 4},
            {"name": "Đồng Hồ Minimalist", "price": 1500000, "img": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800", "cat_idx": 4},
            {"name": "Balo Laptop Đa Năng", "price": 890000, "img": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800", "cat_idx": 4},
        ]

        sizes = ["S", "M", "L", "XL"]
        colors = ["Trắng", "Đen", "Xanh Navy", "Be", "Xám"]

        for prod_data in products_pool:
            # Kiểm tra xem sản phẩm đã có chưa
            if not db.query(models.Product).filter(models.Product.name == prod_data["name"]).first():
                new_prod = models.Product(
                    name=prod_data["name"],
                    description=f"Sản phẩm {prod_data['name']} phong cách trẻ trung, chất liệu bền đẹp, phù hợp cho mọi hoạt động hàng ngày.",
                    price=prod_data["price"],
                    stock=random.randint(10, 50),
                    image_url=prod_data["img"],
                    size=random.choice(sizes),
                    color=random.choice(colors),
                    category_id=category_objects[prod_data["cat_idx"]].id
                )
                db.add(new_prod)

        db.commit()
        print("--- ĐÃ LÀM ĐẦY DỮ LIỆU THÀNH CÔNG ---")
        print(f"- Đã thêm 5 người dùng mẫu.")
        print(f"- Đã thêm 5 danh mục thời trang.")
        print(f"- Đã thêm 30 sản phẩm chất lượng cao.")
    except Exception as e:
        print(f"Lỗi: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
