from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TokenData(BaseModel):
    user_id: Optional[int] = None
    email:   Optional[str] = None

class UserCreate(BaseModel):
    email:     str
    username:  str
    full_name: str
    password:  str
    phone:     Optional[str] = None

class UserLogin(BaseModel):
    email:    str
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone:     Optional[str] = None

class UserResponse(BaseModel):
    id:         int
    email:      str
    username:   str
    full_name:  str
    phone:      Optional[str] = None
    role:       str
    is_active:  bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    user:         UserResponse

class ProductCreate(BaseModel):
    title:       str
    description: Optional[str] = None
    price:       float
    stock:       int
    category:    Optional[str] = None
    image_url:   Optional[str] = None

class ProductUpdate(BaseModel):
    title:       Optional[str]   = None
    description: Optional[str]   = None
    price:       Optional[float] = None
    stock:       Optional[int]   = None
    category:    Optional[str]   = None
    image_url:   Optional[str]   = None
    is_active:   Optional[bool]  = None

class ProductOut(BaseModel):
    id:          int
    title:       str
    description: Optional[str]  = None
    price:       float
    stock:       int
    category:    Optional[str]  = None
    image_url:   Optional[str]  = None
    is_active:   bool
    views:       int
    sold_count:  int
    owner_id:    int
    created_at:  datetime

    class Config:
        from_attributes = True

class ProductPage(BaseModel):
    items:     List[ProductOut]
    total:     int
    page:      int
    page_size: int
    pages:     int
