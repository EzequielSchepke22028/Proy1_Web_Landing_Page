from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
import os

# ─── CONFIGURACIÓN ────────────────────────────────────────

# ⚠️ ANTES (inseguro):
# SECRET_KEY  = os.getenv("SECRET_KEY", "cambiame-en-produccion")
# Si no existía la variable de entorno, usaba esa clave fija.

# ✅ AHORA (seguro):
SECRET_KEY = os.getenv("SECRET_KEY")

# Si no está definida, la aplicación no arranca
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY no configurado")

ALGORITHM   = os.getenv("ALGORITHM", "HS256")
EXPIRE_MINS = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Esquema de hashing — bcrypt es estándar de la industria
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Endpoint donde se obtiene el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


# ─── CONTRASEÑAS ──────────────────────────────────────────

def hash_password(plain_password: str) -> str:
    """Convierte '123456' → hash bcrypt irreversible"""
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara contraseña ingresada con el hash guardado en DB"""
    return pwd_context.verify(plain_password, hashed_password)


# ─── TOKENS JWT ───────────────────────────────────────────

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token JWT firmado.
    data debe contener al menos: {"sub": str(user_id), "email": email}
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=EXPIRE_MINS)
    )

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> schemas.TokenData:
    """Decodifica y valida un token JWT. Lanza excepción si es inválido."""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id: str = payload.get("sub")
        email: str = payload.get("email")

        if user_id is None:
            raise credentials_exception

        return schemas.TokenData(
            user_id=int(user_id),
            email=email
        )

    except JWTError:
        raise credentials_exception


# ─── DEPENDENCIAS FASTAPI ─────────────────────────────────

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.User:
    """
    Dependencia para proteger endpoints.
    Uso: current_user: User = Depends(get_current_user)
    """

    token_data = decode_token(token)

    user = db.query(models.User).filter(
        models.User.id == token_data.user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cuenta desactivada"
        )

    return user


def get_current_seller(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
    """Solo permite acceso a vendedores y admins"""

    if current_user.role not in [
        models.UserRole.seller,
        models.UserRole.admin
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Necesitás ser vendedor para realizar esta acción"
        )

    return current_user


def get_current_admin(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
    """Solo permite acceso a admins"""

    if current_user.role != models.UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso solo para administradores"
        )

    return current_user

"""from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
import os

# ─── CONFIGURACIÓN ────────────────────────────────────────
SECRET_KEY  = os.getenv("SECRET_KEY", "cambiame-en-produccion")
ALGORITHM   = os.getenv("ALGORITHM", "HS256")
EXPIRE_MINS = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Esquema de hashing — bcrypt es el estándar de la industria
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Le dice a FastAPI dónde está el endpoint de login para obtener tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


# ─── CONTRASEÑAS ──────────────────────────────────────────

def hash_password(plain_password: str) -> str:
    """"""Convierte '123456' → '$2b$12$...' (irreversible)"""
"""    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """"""Compara contraseña ingresada con el hash guardado en DB"""
"""    return pwd_context.verify(plain_password, hashed_password)


# ─── TOKENS JWT ───────────────────────────────────────────

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
"""    Crea un token JWT firmado.
    data debe contener al menos: {"sub": str(user_id), "email": email}
    """
"""    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=EXPIRE_MINS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> schemas.TokenData:
    """"""Decodifica y valida un token JWT. Lanza excepción si es inválido.""""""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        email:   str = payload.get("email")
        if user_id is None:
            raise credentials_exception
        return schemas.TokenData(user_id=int(user_id), email=email)
    except JWTError:
        raise credentials_exception


# ─── DEPENDENCIAS FASTAPI ─────────────────────────────────

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.User:
    """
"""    Dependencia para proteger endpoints.
    Uso: current_user: User = Depends(get_current_user)
    """"""
    token_data = decode_token(token)
    user = db.query(models.User).filter(
        models.User.id == token_data.user_id
    ).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cuenta desactivada"
        )
    return user


def get_current_seller(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
    """"""Solo permite acceso a vendedores y admins""""""
    if current_user.role not in [models.UserRole.seller, models.UserRole.admin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Necesitás ser vendedor para realizar esta acción"
        )
    return current_user


def get_current_admin(
    current_user: models.User = Depends(get_current_user)
) -> models.User:
"""
#"""Solo permite acceso a admins"""

""""""

"""
    if current_user.role != models.UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso solo para administradores"
        )
    return current_user"""