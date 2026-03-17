from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from typing import List

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.get("/related/{product_id}", response_model=List[schemas.ProductOut])
def get_related_products(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        return []
    related = db.query(models.Product).filter(
        models.Product.category == product.category,
        models.Product.id != product_id,
        models.Product.is_active == True
    ).order_by(models.Product.views.desc()).limit(4).all()
    return related

@router.get("/trending", response_model=List[schemas.ProductOut])
def get_trending_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).filter(
        models.Product.is_active == True
    ).order_by(models.Product.views.desc()).limit(6).all()
    return products

@router.get("/recent", response_model=List[schemas.ProductOut])
def get_recent_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).filter(
        models.Product.is_active == True
    ).order_by(models.Product.created_at.desc()).limit(6).all()
    return products
