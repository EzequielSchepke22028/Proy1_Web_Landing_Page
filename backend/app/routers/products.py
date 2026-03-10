from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from app.database import get_db
from app import models, schemas
from app.auth import get_current_user

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=schemas.ProductOut, status_code=201)
def create_product(
    payload: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role == models.UserRole.buyer:
        current_user.role = models.UserRole.seller
    product = models.Product(**payload.dict(), owner_id=current_user.id)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.get("/", response_model=schemas.ProductPage)
def list_products(
    search:    Optional[str]   = Query(None),
    category:  Optional[str]   = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    sort_by:   str             = Query("created_at", enum=["price", "created_at", "views"]),
    order:     str             = Query("desc", enum=["asc", "desc"]),
    page:      int             = Query(1, ge=1),
    page_size: int             = Query(12, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(models.Product).filter(models.Product.is_active == True)
    if search:
        query = query.filter(or_(
            models.Product.title.ilike(f"%{search}%"),
            models.Product.description.ilike(f"%{search}%")
        ))
    if category:
        query = query.filter(models.Product.category == category)
    if min_price is not None:
        query = query.filter(models.Product.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)
    sort_col = getattr(models.Product, sort_by)
    query = query.order_by(sort_col.desc() if order == "desc" else sort_col.asc())
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return schemas.ProductPage(
        items=items, total=total, page=page,
        page_size=page_size, pages=(-(-total // page_size))
    )

@router.get("/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(
        models.Product.id == product_id,
        models.Product.is_active == True
    ).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.views += 1
    db.commit()
    db.refresh(product)
    return product

@router.patch("/{product_id}", response_model=schemas.ProductOut)
def update_product(
    product_id: int,
    payload: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your product")
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your product")
    product.is_active = False
    db.commit()
