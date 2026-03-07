from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from app.models import UserRole, OrderStatus

# ─── SCHEMAS DE USUARIO ───────────────────────────────────

class UserCreate(BaseModel):
    """Lo que el cliente manda para registrarse"""
    email:     EmailStr
    username:  str
    full_name: str
    password:  str
    phone:     Optional[str] = None

    @validator("username")
    def username_alphanumeric(cls, v):
        assert v.isalnum(), "El username solo puede tener letras y números"
        assert len(v) >= 3, "El username debe tener al menos 3 caracteres"
        return v.lower()

    @validator("password")
    def password_strength(cls, v):
        assert len(v) >= 8, "La contraseña debe tener al menos 8 caracteres"
        return v


class UserLogin(BaseModel):
    """Lo que el cliente manda para hacer login"""
    email:    EmailStr
    password: str


class UserResponse(BaseModel):
    """Lo que el servidor devuelve (NUNCA incluye la contraseña)"""
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
        from_attributes = True   # permite convertir modelo SQLAlchemy → Pydantic


class UserUpdate(BaseModel):
    """Campos opcionales para actualizar perfil"""
    full_name:  Optional[str] = None
    phone:      Optional[str] = None
    avatar_url: Optional[str] = None


# ─── SCHEMAS DE TOKEN (JWT) ───────────────────────────────

class Token(BaseModel):
    access_token:  str
    token_type:    str = "bearer"
    user:          UserResponse   # devolvemos el usuario junto al token


class TokenData(BaseModel):
    user_id:  Optional[int] = None
    email:    Optional[str] = None


# ─── SCHEMAS DE PRODUCTO ──────────────────────────────────

class ProductCreate(BaseModel):
    title:       str
    description: Optional[str] = None
    price:       float
    stock:       int
    category_id: Optional[int] = None

    @validator("price")
    def price_positive(cls, v):
        assert v > 0, "El precio debe ser mayor a 0"
        return v

    @validator("stock")
    def stock_non_negative(cls, v):
        assert v >= 0, "El stock no puede ser negativo"
        return v


class ProductResponse(BaseModel):
    id:          int
    title:       str
    description: Optional[str]
    price:       float
    stock:       int
    images:      Optional[str]
    views:       int
    sold_count:  int
    seller_id:   int
    category_id: Optional[int]
    created_at:  datetime

    class Config:
        from_attributes = True


# ─── SCHEMAS DE ORDEN ─────────────────────────────────────

class OrderItemCreate(BaseModel):
    product_id: int
    quantity:   int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class OrderResponse(BaseModel):
    id:           int
    status:       OrderStatus
    total_amount: float
    buyer_id:     int
    seller_id:    int
    created_at:   datetime

    class Config:
        from_attributes = True