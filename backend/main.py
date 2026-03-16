# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import users, products, checkout
from app.config import settings

# Crear todas las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MarketEze API",
    version="1.0.0",
    description="Backend del Marketplace",
    # Ocultar documentación en producción por seguridad
    docs_url="/docs" if settings.environment == "development" else None,
    redoc_url="/redoc" if settings.environment == "development" else None,
)

# Configurar CORS según el ambiente
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
]

# En producción, solo permitir tu dominio real
if settings.environment == "production":
    allowed_origins = ["https://tudominio.com"]  # Cambiar cuando tengas dominio

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(users.router)
app.include_router(products.router)
app.include_router(checkout.router)

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "MarketEze API funcionando",
        "version": "1.0.0",
        "environment": settings.environment
    }

@app.get("/health", tags=["Root"])
def health():
    return {"status": "ok"}


"""from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import users, products, checkout
from dotenv import load_dotenv

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MarketEze API", version="1.0.0", description="Backend del Marketplace")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(products.router)
app.include_router(checkout.router)

@app.get("/", tags=["Root"])
def root():
    return {"message": "MarketEze API funcionando", "version": "1.0.0"}

@app.get("/health", tags=["Root"])
def health():
    return {"status": "ok"}"""
