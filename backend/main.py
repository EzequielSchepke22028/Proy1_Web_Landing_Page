from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import users
from dotenv import load_dotenv

load_dotenv()

# Crea todas las tablas en PostgreSQL
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MarketEze API",
    description="Backend del Marketplace",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── ROUTERS ──────────────────────────────────────────────
app.include_router(users.router)

# ─── ENDPOINTS BASE ───────────────────────────────────────
@app.get("/", tags=["Root"])
def root():
    return {"message": "MarketEze API funcionando ✅", "version": "1.0.0"}

@app.get("/health", tags=["Root"])
def health_check():
    return {"status": "ok"}

"""from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from dotenv import load_dotenv

load_dotenv()

# Crea todas las tablas automáticamente
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MarketEze API",
    description="Backend del Marketplace",
    version="1.0.0"
)

# CORS — permite que React (puerto 3001) hable con FastAPI (puerto 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "MarketEze API funcionando ✅", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "ok"}"""