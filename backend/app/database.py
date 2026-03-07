from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Motor de conexión a PostgreSQL
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,        # verifica conexión antes de usarla
    pool_size=10,              # conexiones simultáneas
    max_overflow=20
)

# Sesión para interactuar con la DB
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base para los modelos
Base = declarative_base()

# Dependency — se inyecta en cada endpoint
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()