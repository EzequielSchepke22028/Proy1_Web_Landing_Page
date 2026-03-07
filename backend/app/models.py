from sqlalchemy import (
    Column, Integer, String, Boolean, 
    DateTime, Float, Text, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

# ─── ENUMS ────────────────────────────────────────────────
class UserRole(str, enum.Enum):
    buyer    = "buyer"
    seller   = "seller"
    admin    = "admin"

class OrderStatus(str, enum.Enum):
    pending   = "pending"
    paid      = "paid"
    shipped   = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

# ─── MODELO: USUARIO ──────────────────────────────────────
class User(Base):
    __tablename__ = "users"

    id             = Column(Integer, primary_key=True, index=True)
    email          = Column(String(255), unique=True, index=True, nullable=False)
    username       = Column(String(100), unique=True, index=True, nullable=False)
    full_name      = Column(String(200), nullable=False)
    hashed_password= Column(String(255), nullable=False)
    role           = Column(Enum(UserRole), default=UserRole.buyer)
    is_active      = Column(Boolean, default=True)
    is_verified    = Column(Boolean, default=False)
    avatar_url     = Column(String(500), nullable=True)
    phone          = Column(String(20), nullable=True)
    
    # Reputación del vendedor (0-5)
    reputation     = Column(Float, default=0.0)
    total_sales    = Column(Integer, default=0)

    # Timestamps
    created_at     = Column(DateTime(timezone=True), server_default=func.now())
    updated_at     = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    products       = relationship("Product", back_populates="seller")
    orders_made    = relationship("Order", foreign_keys="Order.buyer_id",  back_populates="buyer")
    orders_received= relationship("Order", foreign_keys="Order.seller_id", back_populates="seller")

    def __repr__(self):
        return f"<User {self.username}>"


# ─── MODELO: CATEGORÍA ────────────────────────────────────
class Category(Base):
    __tablename__ = "categories"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(100), unique=True, nullable=False)
    slug        = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    icon        = Column(String(100), nullable=True)  # nombre del ícono
    
    products    = relationship("Product", back_populates="category")


# ─── MODELO: PRODUCTO ─────────────────────────────────────
class Product(Base):
    __tablename__ = "products"

    id           = Column(Integer, primary_key=True, index=True)
    title        = Column(String(300), nullable=False, index=True)
    description  = Column(Text, nullable=True)
    price        = Column(Float, nullable=False)
    stock        = Column(Integer, default=0)
    is_active    = Column(Boolean, default=True)
    
    # Imágenes (guardamos URLs separadas por coma)
    images       = Column(Text, nullable=True)
    
    # Stats
    views        = Column(Integer, default=0)
    sold_count   = Column(Integer, default=0)

    # Foreign Keys
    seller_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id  = Column(Integer, ForeignKey("categories.id"), nullable=True)

    # Timestamps
    created_at   = Column(DateTime(timezone=True), server_default=func.now())
    updated_at   = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    seller       = relationship("User", back_populates="products")
    category     = relationship("Category", back_populates="products")
    order_items  = relationship("OrderItem", back_populates="product")


# ─── MODELO: ORDEN ────────────────────────────────────────
class Order(Base):
    __tablename__ = "orders"

    id           = Column(Integer, primary_key=True, index=True)
    status       = Column(Enum(OrderStatus), default=OrderStatus.pending)
    total_amount = Column(Float, nullable=False)
    
    # MercadoPago
    mp_payment_id= Column(String(100), nullable=True)

    # Foreign Keys
    buyer_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    seller_id    = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Timestamps
    created_at   = Column(DateTime(timezone=True), server_default=func.now())
    updated_at   = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    buyer        = relationship("User", foreign_keys=[buyer_id],  back_populates="orders_made")
    seller       = relationship("User", foreign_keys=[seller_id], back_populates="orders_received")
    items        = relationship("OrderItem", back_populates="order")


# ─── MODELO: ITEM DE ORDEN ────────────────────────────────
class OrderItem(Base):
    __tablename__ = "order_items"

    id         = Column(Integer, primary_key=True, index=True)
    quantity   = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    order_id   = Column(Integer, ForeignKey("orders.id"),   nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    order      = relationship("Order",   back_populates="items")
    product    = relationship("Product", back_populates="order_items")