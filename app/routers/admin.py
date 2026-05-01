from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas, auth

router = APIRouter(prefix="/admin", tags=["Admin API"])

# --- Quản lý Sản phẩm ---
@router.get("/products", response_model=List[schemas.Product])
def admin_get_products(db: Session = Depends(get_db), current_admin: models.User = Depends(auth.get_current_admin)):
    return db.query(models.Product).all()

@router.post("/products", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), current_admin: models.User = Depends(auth.get_current_admin)):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.put("/products/{id}", response_model=schemas.Product)
def update_product(id: int, product_update: schemas.ProductUpdate, db: Session = Depends(get_db), current_admin: models.User = Depends(auth.get_current_admin)):
    db_product = db.query(models.Product).filter(models.Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")
    
    update_data = product_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db), current_admin: models.User = Depends(auth.get_current_admin)):
    db_product = db.query(models.Product).filter(models.Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")
    db.delete(db_product)
    db.commit()
    return {"message": "Đã xóa sản phẩm thành công"}

# --- Quản lý Danh mục ---
@router.get("/categories", response_model=List[schemas.Category])
def admin_get_categories(db: Session = Depends(get_db), current_admin: models.User = Depends(auth.get_current_admin)):
    return db.query(models.Category).all()

@router.post("/categories", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db), current_admin: models.User = Depends(auth.get_current_admin)):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.put("/categories/{id}", response_model=schemas.Category)
def update_category(id: int, category_update: schemas.CategoryUpdate, db: Session = Depends(get_db), current_admin: models.User = Depends(auth.get_current_admin)):
    db_category = db.query(models.Category).filter(models.Category.id == id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Không tìm thấy danh mục")
    
    update_data = category_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)
    
    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/categories/{id}")
def delete_category(id: int, db: Session = Depends(get_db), current_admin: models.User = Depends(auth.get_current_admin)):
    db_category = db.query(models.Category).filter(models.Category.id == id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Không tìm thấy danh mục")
    db.delete(db_category)
    db.commit()
    return {"message": "Đã xóa danh mục thành công"}

# --- Quản lý Đơn hàng ---
@router.get("/orders", response_model=List[schemas.Order])
def get_all_orders(db: Session = Depends(get_db), current_admin: models.User = Depends(auth.get_current_admin)):
    return db.query(models.Order).all()

@router.patch("/orders/{id}/status", response_model=schemas.Order)
def update_order_status(id: int, status_update: schemas.OrderStatusUpdate, db: Session = Depends(get_db), current_admin: models.User = Depends(auth.get_current_admin)):
    db_order = db.query(models.Order).filter(models.Order.id == id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")
    db_order.status = status_update.status
    db.commit()
    db.refresh(db_order)
    return db_order

@router.delete("/orders/{id}")
def delete_order(id: int, db: Session = Depends(get_db), current_admin: models.User = Depends(auth.get_current_admin)):
    db_order = db.query(models.Order).filter(models.Order.id == id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")
    db.delete(db_order)
    db.commit()
    return {"message": "Đã xóa đơn hàng thành công"}

# --- Quản lý Người dùng ---
@router.get("/users", response_model=List[schemas.User])
def get_all_users(db: Session = Depends(get_db), current_admin: models.User = Depends(auth.get_current_admin)):
    return db.query(models.User).all()

@router.put("/users/{id}/role", response_model=schemas.User)
def update_user_role(id: int, role_update: schemas.UserUpdateRole, db: Session = Depends(get_db), current_admin: models.User = Depends(auth.get_current_admin)):
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
    db_user.role = role_update.role
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{id}")
def delete_user(id: int, db: Session = Depends(get_db), current_admin: models.User = Depends(auth.get_current_admin)):
    db_user = db.query(models.User).filter(models.User.id == id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")
    db.delete(db_user)
    db.commit()
    return {"message": "Đã xóa người dùng thành công"}
