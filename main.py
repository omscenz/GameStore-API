import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials

from routes.contracts import router as contracts_router
from routes.contracts_types import router as contract_types_router
from routes.users import router as users_router, login_router


app = FastAPI(
    title="API Proyecto Final",
    description="API REST para manejo de Modelo Principal y Tipos",
    version="1.0.0"
)

# Configuración CORS 
origins = [
    "http://localhost",
    "http://localhost:3000",  
   
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(contracts_router)
app.include_router(contract_types_router)
app.include_router(users_router)
app.include_router(login_router)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
def read_root():
    return {"status": "healthy", "version": "0.0.0", "service": "API Proyecto Final"}

app.get("/health")
def health_check():
    try:
        return { 
            "status": "healthy",
            "timestamp": "2025-01-31",
            "service": "API Proyecto Final",
            "environment": "production"
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
    
@app.get("/ready")
def readiness_check():
    try:
           from utils.mongobd import test_connection
           db_status = test_connection()
           return {
               "status": "ready" if db_status else "not ready",
               "database": "connected" if db_status else "disconnected",
               "service": "API Proyecto Final",
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


@app.on_event("startup")
async def startup_db_client():
  
    
    pass


@app.on_event("shutdown")
async def shutdown_db_client():

    pass


@app.get("/", tags=["Root"])
async def root():
    return {"message": "API Proyecto Final funcionando"}

