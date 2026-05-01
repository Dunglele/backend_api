from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdateRole(BaseModel):
    role: str

class User(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

# Category Schemas
class CategoryBase(BaseModel):
    name: str
    image_url: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    image_url: Optional[str] = None

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True

# Product Schemas
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    image_url: Optional[str] = None
    size: Optional[str] = None
    color: Optional[str] = None
    category_id: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    image_url: Optional[str] = None
    size: Optional[str] = None
    color: Optional[str] = None
    category_id: Optional[int] = None

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True

# Order Schemas
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    price: float

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    pass

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderStatusUpdate(BaseModel):
    status: str

class Order(OrderBase):
    id: int
    user_id: int
    total_price: float
    status: str
    created_at: datetime
    items: List[OrderItem]

    class Config:
        from_attributes = True

# Wishlist Schemas
class WishlistBase(BaseModel):
    product_id: int

class WishlistCreate(WishlistBase):
    pass

class Wishlist(WishlistBase):
    id: int
    user_id: int
    product: Product # Bao gồm thông tin sản phẩm trong wishlist

    class Config:
        from_attributes = True
