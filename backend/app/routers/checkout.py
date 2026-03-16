from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from app.database import get_db
from app import models
from app.auth import get_current_user
import mercadopago
import os

router = APIRouter(prefix="/checkout", tags=["Checkout"])

class CheckoutItem(BaseModel):
    product_id: int
    quantity:   int

class CheckoutRequest(BaseModel):
    items: List[CheckoutItem]

@router.post("/create-preference")
def create_preference(
    payload: CheckoutRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    mp_token = os.getenv("MP_ACCESS_TOKEN")
    sdk = mercadopago.SDK(mp_token)

    mp_items = []
    for item in payload.items:
        product = db.query(models.Product).filter(
            models.Product.id == item.product_id,
            models.Product.is_active == True
        ).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Producto {item.product_id} no encontrado")

        mp_items.append({
            "id":          str(product.id),
            "title":       product.title,
            "quantity":    item.quantity,
            "unit_price":  float(product.price),
            "currency_id": "ARS",
        })

    preference_data = {
        "items": mp_items,
        "payer": { "email": current_user.email },
        "external_reference": str(current_user.id),
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]

    if "id" not in preference:
        raise HTTPException(status_code=500, detail=f"Error MP: {preference}")

    return {
        "preference_id":      preference["id"],
        "init_point":         preference["init_point"],
        "sandbox_init_point": preference.get("sandbox_init_point", preference["init_point"]),
    }
