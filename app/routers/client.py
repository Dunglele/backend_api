from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from .. import models, schemas, auth

router = APIRouter(tags=["Client API"])

@router.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email đã được đăng ký")
    
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        role="user" # Mặc định là user
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=schemas.Token)
def login(form_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.email).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/products", response_model=List[schemas.Product])
def get_products(category_id: Optional[int] = None, search: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Product)
    if category_id:
        query = query.filter(models.Product.category_id == category_id)
    if search:
        query = query.filter(models.Product.name.contains(search))
    return query.all()

@router.get("/categories", response_model=List[schemas.Category])
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()

@router.post("/orders", response_model=schemas.Order)
def place_order(order_data: schemas.OrderCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    total_price = 0
    order_items = []
    
    for item in order_data.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Sản phẩm ID {item.product_id} không tồn tại")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Sản phẩm {product.name} không đủ hàng")
        
        # Cập nhật kho
        product.stock -= item.quantity
        
        price = product.price
        total_price += price * item.quantity
        order_items.append(models.OrderItem(
            product_id=item.product_id,
            quantity=item.quantity,
            price=price
        ))

    new_order = models.Order(
        user_id=current_user.id,
        total_price=total_price,
        status="pending",
        items=order_items
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

# --- Wishlist API ---
@router.get("/wishlist", response_model=List[schemas.Wishlist])
def get_wishlist(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Wishlist).filter(models.Wishlist.user_id == current_user.id).all()

@router.post("/wishlist/{product_id}", response_model=schemas.Wishlist)
def add_to_wishlist(product_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Kiểm tra sản phẩm có tồn tại không
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")
    
    # Kiểm tra xem đã có trong wishlist chưa
    existing = db.query(models.Wishlist).filter(
        models.Wishlist.user_id == current_user.id,
        models.Wishlist.product_id == product_id
    ).first()
    if existing:
        return existing
    
    new_wish = models.Wishlist(user_id=current_user.id, product_id=product_id)
    db.add(new_wish)
    db.commit()
    db.refresh(new_wish)
    return new_wish

@router.delete("/wishlist/{product_id}")
def remove_from_wishlist(product_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    wish_item = db.query(models.Wishlist).filter(
        models.Wishlist.user_id == current_user.id,
        models.Wishlist.product_id == product_id
    ).first()
    if not wish_item:
        raise HTTPException(status_code=404, detail="Sản phẩm không có trong danh sách yêu thích")
    
    db.delete(wish_item)
    db.commit()
    return {"message": "Đã bỏ sản phẩm khỏi danh sách yêu thích"}
