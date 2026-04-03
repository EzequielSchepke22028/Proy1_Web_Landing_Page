from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.auth import get_current_user
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/orders", tags=["Orders"])

class OrderItemOut(BaseModel):
    id:         int
    product_id: int
    quantity:   int
    unit_price: float
    product_title: Optional[str] = None
    product_image: Optional[str] = None

    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    id:               int
    status:           str
    total_amount:     float
    mp_payment_id:    Optional[str] = None
    created_at:       datetime
    items:            List[OrderItemOut] = []

    class Config:
        from_attributes = True

@router.get("/mine", response_model=List[OrderOut])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    orders = db.query(models.Order).filter(
        models.Order.buyer_id == current_user.id
    ).order_by(models.Order.created_at.desc()).all()

    result = []
    for order in orders:
        items = []
        for item in order.items:
            product = db.query(models.Product).filter(
                models.Product.id == item.product_id
            ).first()
            items.append(OrderItemOut(
                id=item.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                product_title=product.title if product else "Producto eliminado",
                product_image=product.image_url if product else None,
            ))
        result.append(OrderOut(
            id=order.id,
            status=order.status,
            total_amount=order.total_amount,
            mp_payment_id=order.mp_payment_id,
            created_at=order.created_at,
            items=items,
        ))
    return result
