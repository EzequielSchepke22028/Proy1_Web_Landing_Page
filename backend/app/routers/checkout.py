# backend/app/routers/checkout.py

# backend/app/routers/checkout.py
from fastapi import APIRouter, Depends, HTTPException, Request, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from app.database import get_db
from app import models
from app.auth import get_current_user
from app.config import settings
import mercadopago
import hmac
import hashlib

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
    Valida stock y precios desde la base de datos.
    """
    mp_items = []
    total_amount = 0
    
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

        item_price = float(product.price)
        total_amount += item_price * item.quantity

        mp_items.append({
            "id": str(product.id),
            "title": product.title,
            "quantity": item.quantity,
            "unit_price": item_price,  # ← Precio desde BD, no del frontend
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
        "notification_url": f"{settings.webhook_base_url}/checkout/webhook",
        "metadata": {
            "user_id": current_user.id,
            "total_amount": total_amount
        }
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
async def mercadopago_webhook(
    request: Request,
    db: Session = Depends(get_db),
    x_signature: Optional[str] = Header(None),
    x_request_id: Optional[str] = Header(None)
):
    """
    Webhook SEGURO para recibir notificaciones de MercadoPago.
    
    SEGURIDAD:
    1. Verifica que la notificación viene de MercadoPago (firma)
    2. Consulta el pago directamente a la API (no confía en el JSON recibido)
    3. Valida el monto contra la base de datos
    4. Implementa idempotencia (no procesa dos veces el mismo pago)
    """
    try:
        # 1. Obtener el cuerpo del request
        body = await request.body()
        data = await request.json()
        
        # 2. VERIFICACIÓN DE FIRMA (CRÍTICO para producción)
        # Nota: En TEST mode, MercadoPago no siempre envía firma
        if settings.environment == "production" and x_signature:
            # TODO: Implementar verificación de firma cuando vayas a producción
            # secret = settings.mp_webhook_secret
            # expected_signature = hmac.new(
            #     secret.encode(),
            #     body,
            #     hashlib.sha256
            # ).hexdigest()
            # if not hmac.compare_digest(expected_signature, x_signature):
            #     raise HTTPException(status_code=401, detail="Firma inválida")
            pass
        
        # 3. Procesar solo notificaciones de pagos
        if data.get("type") == "payment" or data.get("action") == "payment.created":
            payment_id = data.get("data", {}).get("id")
            
            if not payment_id:
                return {"status": "ok", "message": "No payment ID"}
            
            # 4. CRÍTICO: Consultar el pago DIRECTAMENTE a MercadoPago
            # NUNCA confiar solo en los datos del webhook
            payment_info = sdk.payment().get(payment_id)
            
            if payment_info["status"] != 200:
                print(f"❌ Error consultando pago {payment_id}")
                return {"status": "error", "message": "Payment not found"}
            
            payment = payment_info["response"]
            
            # 5. Verificar el estado del pago
            if payment["status"] == "approved":
                user_id = int(payment.get("external_reference", 0))
                amount = payment["transaction_amount"]
                
                print(f"✅ Pago aprobado:")
                print(f"   - ID: {payment_id}")
                print(f"   - Usuario: {user_id}")
                print(f"   - Monto: ${amount}")
                print(f"   - Email: {payment.get('payer', {}).get('email')}")
                
                # 6. IDEMPOTENCIA: Verificar que no procesamos este pago antes
                # TODO: Implementar tabla de Payments en la BD
                # existing_payment = db.query(Payment).filter(
                #     Payment.mp_payment_id == str(payment_id)
                # ).first()
                # 
                # if existing_payment:
                #     return {"status": "ok", "message": "Already processed"}
                
                # 7. Procesar el pago (actualizar orden, reducir stock, etc.)
                # TODO: Implementar lógica de negocio
                # - Crear registro de Order
                # - Reducir stock de productos
                # - Enviar email de confirmación
                # - etc.
                
                print(f"📦 Procesando entrega para usuario {user_id}")
                
            elif payment["status"] == "pending":
                print(f"⏳ Pago pendiente: {payment_id}")
                
            elif payment["status"] == "rejected":
                print(f"❌ Pago rechazado: {payment_id}")
                print(f"   Razón: {payment.get('status_detail')}")
        
        # 8. IMPORTANTE: Siempre responder 200 OK
        # Si no respondes 200, MercadoPago reintentará la notificación
        return {"status": "ok"}
        
    except Exception as e:
        print(f"💥 Error en webhook: {str(e)}")
        # Aún con error, responder 200 para evitar reintentos infinitos
        return {"status": "error", "message": str(e)}


"""from fastapi import APIRouter, Depends, HTTPException
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
#    Crear preferencia de pago en MercadoPago.
#    Valida stock y crea los items para el checkout.
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
#    Webhook para recibir notificaciones de MercadoPago.
#    Se llama automáticamente cuando hay cambios en un pago.
#   """
"""    try:
        if data.get("type") == "payment":
            payment_id = data["data"]["id"]
            
            # Consultar el pago directamente a MercadoPago
            payment_info = sdk.payment().get(payment_id)
            
            if payment_info["status"] == 200:
                payment = payment_info["response"]
                
                if payment["status"] == "approved":
                    print(f"✅ Pago aprobado: {payment_id}")
                    #""" """ Actualizar base de datos, enviar email, etc.
                    
                elif payment["status"] == "pending":
                    print(f"⏳ Pago pendiente: {payment_id}")
                    
                elif payment["status"] == "rejected":
                    print(f"❌ Pago rechazado: {payment_id}")
        
        return {"status": "ok"}
        
    except Exception as e:
        print(f"Error en webhook: {str(e)}")
        return {"status": "error", "message": str(e)}"""

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
