from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import enum

class UserRole(str, enum.Enum):
    buyer  = "buyer"
    seller = "seller"
    admin  = "admin"

class OrderStatus(str, enum.Enum):
    pending   = "pending"
    paid      = "paid"
    shipped   = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

class User(Base):
    __tablename__ = "users"
    id              = Column(Integer, primary_key=True, index=True)
    email           = Column(String, unique=True, index=True, nullable=False)
    username        = Column(String, unique=True, index=True, nullable=False)
    full_name       = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    phone           = Column(String, nullable=True)
    role            = Column(Enum(UserRole), default=UserRole.buyer)
    is_active       = Column(Boolean, default=True)
    created_at      = Column(DateTime, default=datetime.utcnow)
    products        = relationship("Product", back_populates="owner")
    orders_made     = relationship("Order", foreign_keys="Order.buyer_id",  back_populates="buyer")
    orders_received = relationship("Order", foreign_keys="Order.seller_id", back_populates="seller")

class Product(Base):
    __tablename__ = "products"
    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price       = Column(Float, nullable=False)
    stock       = Column(Integer, default=0)
    category    = Column(String, nullable=True)
    image_url   = Column(String, nullable=True)
    is_active   = Column(Boolean, default=True)
    views       = Column(Integer, default=0)
    sold_count  = Column(Integer, default=0)
    owner_id    = Column(Integer, ForeignKey("users.id"))
    created_at  = Column(DateTime, default=datetime.utcnow)
    owner       = relationship("User", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")

class Order(Base):
    __tablename__ = "orders"
    id                  = Column(Integer, primary_key=True, index=True)
    buyer_id            = Column(Integer, ForeignKey("users.id"))
    seller_id           = Column(Integer, ForeignKey("users.id"), nullable=True)
    status              = Column(Enum(OrderStatus), default=OrderStatus.pending)
    total_amount        = Column(Float, nullable=False)
    mp_payment_id       = Column(String, nullable=True)
    mp_preference_id    = Column(String, nullable=True)
    created_at          = Column(DateTime, default=datetime.utcnow)
    updated_at          = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    buyer               = relationship("User", foreign_keys=[buyer_id],  back_populates="orders_made")
    seller              = relationship("User", foreign_keys=[seller_id], back_populates="orders_received")
    items               = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id         = Column(Integer, primary_key=True, index=True)
    order_id   = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity   = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    order      = relationship("Order",   back_populates="items")
    product    = relationship("Product", back_populates="order_items")
