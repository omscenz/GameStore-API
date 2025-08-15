from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
import uvicorn
from main import app

import uvicorn

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

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    return {"message": "API Proyecto Final funcionando"}

# Health endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    return { 
        "status": "healthy",
        "service": "API Proyecto Final",
        "environment": "production"
    }

# Readiness endpoint
@app.get("/ready", tags=["Health"])
async def readiness_check():
    try:
        from utils.mongodb import test_connection
        db_status = test_connection()
        return {
            "status": "ready" if db_status else "not ready",
            "database": "connected" if db_status else "disconnected",
            "service": "API Proyecto Final",
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
    
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))  # Railway define la variable PORT
    uvicorn.run(app, host="0.0.0.0", port=port)
