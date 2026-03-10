from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from app.models import UserRole, OrderStatus

class UserCreate(BaseModel):
    email:     EmailStr
    username:  str
    full_name: str
    password:  str
    phone:     Optional[str] = None

    @validator("username")
    def username_alphanumeric(cls, v):
        assert v.isalnum(), "El username solo puede tener letras y numeros"
        assert len(v) >= 3, "El username debe tener al menos 3 caracteres"
        return v.lower()

    @validator("password")
    def password_strength(cls, v):
        assert len(v) >= 8, "La contrasena debe tener al menos 8 caracteres"
        return v

class UserLogin(BaseModel):
    email:    EmailStr
    password: str

class UserResponse(BaseModel):
    id:          int
    email:       str
    username:    str
    full_name:   str
    role:        UserRole
    is_active:   bool
    is_verified: bool
    avatar_url:  Optional[str]
    phone:       Optional[str]
    reputation:  float
    total_sales: int
    created_at:  datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name:  Optional[str] = None
    phone:      Optional[str] = None
    avatar_url: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type:   str = "bearer"
    user:         UserResponse

class TokenData(BaseModel):
    user_id: Optional[int] = None
    email:   Optional[str] = None

VALID_CATEGORIES = [
    "Electronics", "Clothing", "Home & Garden", "Sports",
    "Books", "Toys", "Vehicles", "Services", "Other"
]

class ProductCreate(BaseModel):
    title:       str
    description: Optional[str] = None
    price:       Decimal
    stock:       int
    category:    Optional[str] = None
    image_url:   Optional[str] = None

    @validator("title")
    def title_not_empty(cls, v):
        v = v.strip()
        assert len(v) >= 3, "Title must be at least 3 characters"
        return v

    @validator("price")
    def price_positive(cls, v):
        assert v > 0, "Price must be greater than 0"
        return round(v, 2)

    @validator("stock")
    def stock_non_negative(cls, v):
        assert v >= 0, "Stock cannot be negative"
        return v

    class Config:
        json_encoders = {Decimal: str}

class ProductUpdate(BaseModel):
    title:       Optional[str]     = None
    description: Optional[str]     = None
    price:       Optional[Decimal] = None
    stock:       Optional[int]     = None
    category:    Optional[str]     = None
    image_url:   Optional[str]     = None

class ProductOut(BaseModel):
    id:          int
    title:       str
    description: Optional[str]
    price:       Decimal
    stock:       int
    category:    Optional[str]
    image_url:   Optional[str]
    views:       int
    sold_count:  int
    owner_id:    int
    is_active:   bool
    created_at:  datetime

    class Config:
        from_attributes = True
        json_encoders   = {Decimal: str}

class ProductPage(BaseModel):
    items:     List[ProductOut]
    total:     int
    page:      int
    page_size: int
    pages:     int

class OrderItemCreate(BaseModel):
    product_id: int
    quantity:   int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderResponse(BaseModel):
    id:           int
    status:       OrderStatus
    total_amount: Decimal
    buyer_id:     int
    seller_id:    int
    created_at:   datetime

    class Config:
        from_attributes = True
