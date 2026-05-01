import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_workflow():
    print("--- BẮT ĐẦU KIỂM THỬ WORKFLOW API ---")
    
    # 1. Đăng ký tài khoản khách hàng mới
    client_email = "customer@example.com"
    client_pass = "password123"
    reg_response = requests.post(f"{BASE_URL}/register", json={
        "email": client_email,
        "password": client_pass,
        "full_name": "Nguyen Van Khach"
    })
    print(f"1. Đăng ký khách hàng: {reg_response.status_code}")

    # 2. Đăng nhập Admin (Lấy từ file admin_account.txt đã tạo)
    admin_login = requests.post(f"{BASE_URL}/login", json={
        "email": "admin@shop.com",
        "password": "admin12345"
    })
    admin_token = admin_login.json().get("access_token")
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    print(f"2. Đăng nhập Admin: {admin_login.status_code}")

    # 3. Admin tạo Danh mục
    cat_response = requests.post(f"{BASE_URL}/admin/categories", headers=admin_headers, json={
        "name": "Thời trang Nam",
        "image_url": "http://image.com/nam.jpg"
    })
    category_id = cat_response.json().get("id")
    print(f"3. Admin tạo danh mục (ID={category_id}): {cat_response.status_code}")

    # 4. Admin tạo Sản phẩm
    prod_response = requests.post(f"{BASE_URL}/admin/products", headers=admin_headers, json={
        "name": "Áo sơ mi trắng",
        "description": "Chất liệu cotton cao cấp",
        "price": 250000,
        "stock": 100,
        "category_id": category_id,
        "size": "L",
        "color": "Trắng"
    })
    product_id = prod_response.json().get("id")
    print(f"4. Admin tạo sản phẩm (ID={product_id}): {prod_response.status_code}")

    # 5. Khách hàng đăng nhập
    client_login = requests.post(f"{BASE_URL}/login", json={
        "email": client_email,
        "password": client_pass
    })
    client_token = client_login.json().get("access_token")
    client_headers = {"Authorization": f"Bearer {client_token}"}
    print(f"5. Khách hàng đăng nhập: {client_login.status_code}")

    # 6. Khách hàng xem danh sách sản phẩm
    list_prod = requests.get(f"{BASE_URL}/products")
    print(f"6. Xem sản phẩm: {len(list_prod.json())} sản phẩm tìm thấy.")

    # 7. Khách hàng đặt hàng
    order_response = requests.post(f"{BASE_URL}/orders", headers=client_headers, json={
        "items": [
            {"product_id": product_id, "quantity": 2}
        ]
    })
    print(f"7. Đặt hàng: {order_response.status_code} - Tổng tiền: {order_response.json().get('total_price')}")

    # 8. Admin kiểm tra đơn hàng mới
    orders_list = requests.get(f"{BASE_URL}/admin/orders", headers=admin_headers)
    print(f"8. Admin xem đơn hàng: {len(orders_list.json())} đơn hàng tồn tại.")

    print("--- KIỂM THỬ HOÀN TẤT ---")

if __name__ == "__main__":
    try:
        test_workflow()
    except Exception as e:
        print(f"Lỗi khi kiểm thử: {e}")
        print("Lưu ý: Hãy đảm bảo server đang chạy tại http://127.0.0.1:8000")
