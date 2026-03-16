# backend/app/config.py
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from functools import lru_cache

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    """Configuración centralizada de la aplicación"""
    
    # Database
    database_url: str
    
    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Redis
    redis_url: str
    
    # MercadoPago
    mp_access_token: str
    mp_public_key: str = ""
    
    # Environment
    environment: str = "development"
    
    # Webhooks
    webhook_base_url: str = "http://localhost:8080"  # ← NUEVO
    
    class Config:
        env_file = str(BASE_DIR / ".env")
        env_file_encoding = 'utf-8'
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """Singleton de settings"""
    return Settings()

settings = get_settings()

# backend/app/config.py
"""import os
from pathlib import Path
from pydantic_settings import BaseSettings
from functools import lru_cache

# Ruta base del proyecto backend
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    """ 
#    """Configuración centralizada de la aplicación. Lee automáticamente las variables desde el archivo .env """ 
    
"""
    
    # Database
    database_url: str
    
    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Redis
    redis_url: str
    
    # MercadoPago
    mp_access_token: str
    mp_public_key: str = ""
    
    # Environment (development, staging, production)
    environment: str = "development"
    
    class Config:
        env_file = str(BASE_DIR / ".env")
        env_file_encoding = 'utf-8'
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """ 
#    """Retorna una instancia singleton de Settings. Se cachea para evitar leer el .env múltiples veces."""    """
#    return Settings()

# Instancia global que se importa en toda la app
#settings = get_settings()