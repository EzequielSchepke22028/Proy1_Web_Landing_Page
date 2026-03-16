# backend/app/routers/checkout.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from app.database import get_db
from app import models
from app.auth import get_current_user
from app.config import settings
import mercadopago

router = APIRouter(prefix="/checkout", tags=["Checkout"])

# Inicializar SDK de MercadoPago con settings
sdk = mercadopago.SDK(settings.mp_access_token)

class CheckoutItem(BaseModel):
    product_id: int
    quantity: int

class CheckoutRequest(BaseModel):
    items: List[CheckoutItem]

@router.post("/create-preference")
def create_preference(
    payload: CheckoutRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Crear preferencia de pago en MercadoPago.
    Valida stock y crea los items para el checkout.
    """
    mp_items = []
    
    # Validar y construir items
    for item in payload.items:
        product = db.query(models.Product).filter(
            models.Product.id == item.product_id,
            models.Product.is_active == True
        ).first()
        
        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Producto {item.product_id} no encontrado"
            )
        
        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente para {product.title}"
            )

        mp_items.append({
            "id": str(product.id),
            "title": product.title,
            "quantity": item.quantity,
            "unit_price": float(product.price),
            "currency_id": "ARS",
        })

    # Crear preferencia en MercadoPago
    preference_data = {
        "items": mp_items,
        "payer": {"email": current_user.email},
        "back_urls": {
            "success": "http://localhost:3000/checkout/success",
            "failure": "http://localhost:3000/checkout/failure",
            "pending": "http://localhost:3000/checkout/pending",
        },
        "auto_return": "approved",
        "external_reference": str(current_user.id),
    }

    try:
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response["response"]

        if "id" not in preference:
            raise HTTPException(
                status_code=500,
                detail=f"Error al crear preferencia: {preference}"
            )

        return {
            "preference_id": preference["id"],
            "init_point": preference["init_point"],
            "sandbox_init_point": preference.get(
                "sandbox_init_point",
                preference["init_point"]
            ),
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error de MercadoPago: {str(e)}"
        )

@router.post("/webhook")
async def mercadopago_webhook(data: dict):
    """
    Webhook para recibir notificaciones de MercadoPago.
    Se llama automáticamente cuando hay cambios en un pago.
    """
    try:
        if data.get("type") == "payment":
            payment_id = data["data"]["id"]
            
            # Consultar el pago directamente a MercadoPago
            payment_info = sdk.payment().get(payment_id)
            
            if payment_info["status"] == 200:
                payment = payment_info["response"]
                
                if payment["status"] == "approved":
                    print(f"✅ Pago aprobado: {payment_id}")
                    # TODO: Actualizar base de datos, enviar email, etc.
                    
                elif payment["status"] == "pending":
                    print(f"⏳ Pago pendiente: {payment_id}")
                    
                elif payment["status"] == "rejected":
                    print(f"❌ Pago rechazado: {payment_id}")
        
        return {"status": "ok"}
        
    except Exception as e:
        print(f"Error en webhook: {str(e)}")
        return {"status": "error", "message": str(e)}

"""from fastapi import APIRouter, Depends, HTTPException
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
    }"""
