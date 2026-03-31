from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.auth import hash_password, verify_password, create_access_token, get_current_user
import httpx

router = APIRouter(prefix="/users", tags=["Users"])

N8N_WEBHOOK_URL = "http://localhost:5678/webhook/user-registered"

@router.post("/register", response_model=schemas.Token, status_code=201)
def register(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email ya registrado")
    if db.query(models.User).filter(models.User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username ya existe")
    user = models.User(
        email=payload.email,
        username=payload.username,
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password),
        phone=payload.phone,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token({"sub": str(user.id), "email": user.email})
    try:
        httpx.post(N8N_WEBHOOK_URL, json={
            "email":     user.email,
            "username":  user.username,
            "full_name": user.full_name,
        }, timeout=3)
    except Exception:
        pass
    return schemas.Token(
        access_token=token,
        user=schemas.UserResponse.from_orm(user)
    )

@router.post("/login", response_model=schemas.Token)
def login(payload: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    token = create_access_token({"sub": str(user.id), "email": user.email})
    return schemas.Token(
        access_token=token,
        user=schemas.UserResponse.from_orm(user)
    )

@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=schemas.UserResponse)
def update_me(
    payload: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.post("/become-seller", response_model=schemas.UserResponse)
def become_seller(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    current_user.role = models.UserRole.seller
    db.commit()
    db.refresh(current_user)
    return current_user
