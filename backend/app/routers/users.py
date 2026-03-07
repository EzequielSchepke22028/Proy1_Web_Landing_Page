from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)

router = APIRouter(prefix="/users", tags=["Usuarios"])


# ─── REGISTRO ─────────────────────────────────────────────

@router.post(
    "/register",
    response_model=schemas.Token,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario"
)
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):

    # 1. Verificar que el email no exista
    if db.query(models.User).filter(models.User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una cuenta con ese email"
        )

    # 2. Verificar que el username no exista
    if db.query(models.User).filter(models.User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ese nombre de usuario ya está en uso"
        )

    # 3. Crear usuario con contraseña hasheada
    new_user = models.User(
        email           = user_data.email,
        username        = user_data.username,
        full_name       = user_data.full_name,
        hashed_password = hash_password(user_data.password),
        phone           = user_data.phone,
        role            = models.UserRole.buyer  # por defecto es comprador
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 4. Generar token JWT automáticamente al registrarse
    token = create_access_token(data={
        "sub":   str(new_user.id),
        "email": new_user.email
    })

    return schemas.Token(
        access_token=token,
        token_type="bearer",
        user=new_user
    )


# ─── LOGIN ────────────────────────────────────────────────

@router.post(
    "/login",
    response_model=schemas.Token,
    summary="Iniciar sesión"
)
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):

    # 1. Buscar usuario por email
    user = db.query(models.User).filter(
        models.User.email == credentials.email
    ).first()

    # 2. Verificar contraseña
    # Usamos el mismo mensaje para email y contraseña incorrectos
    # para no dar pistas a posibles atacantes
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )

    # 3. Verificar que la cuenta esté activa
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tu cuenta está desactivada. Contactá al soporte."
        )

    # 4. Generar y devolver token
    token = create_access_token(data={
        "sub":   str(user.id),
        "email": user.email
    })

    return schemas.Token(
        access_token=token,
        token_type="bearer",
        user=user
    )


# ─── PERFIL ───────────────────────────────────────────────

@router.get(
    "/me",
    response_model=schemas.UserResponse,
    summary="Ver mi perfil"
)
def get_my_profile(current_user: models.User = Depends(get_current_user)):
    """Endpoint protegido — requiere token JWT válido"""
    return current_user


@router.put(
    "/me",
    response_model=schemas.UserResponse,
    summary="Actualizar mi perfil"
)
def update_my_profile(
    updates: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Solo actualiza los campos que se enviaron
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)
    return current_user


@router.post(
    "/become-seller",
    response_model=schemas.UserResponse,
    summary="Convertirse en vendedor"
)
def become_seller(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Permite a un comprador convertirse en vendedor"""
    if current_user.role == models.UserRole.seller:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya sos vendedor"
        )
    current_user.role = models.UserRole.seller
    db.commit()
    db.refresh(current_user)
    return current_user