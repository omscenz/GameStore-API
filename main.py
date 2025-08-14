from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials

from routes.contracts import router as contracts_router
from routes.contracts_types import router as contract_types_router
from routes.users import router as users_router, login_router



#cred = credentials.Certificate("secrets/firebase_credentials.json")
#firebase_admin.initialize_app(cred)

app = FastAPI(
    title="API Proyecto Final",
    description="API REST para manejo de Modelo Principal y Tipos",
    version="1.0.0"
)

# Configuración CORS (ajusta dominios según frontend)
origins = [
    "http://localhost",
    "http://localhost:3000",  # si usas React localmente
    # agrega aquí la URL de tu frontend desplegado en GitHub Pages
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

# Evento para startup (si quieres conectar o probar conexión a MongoDB aquí)
@app.on_event("startup")
async def startup_db_client():
    # Si usas conexión global, inicia aquí
    # Ejemplo: await mongodb_client.connect()
    pass

# Evento para shutdown (cerrar conexión)
@app.on_event("shutdown")
async def shutdown_db_client():
    # Ejemplo: await mongodb_client.close()
    pass

# Ruta raíz simple
@app.get("/", tags=["Root"])
async def root():
    return {"message": "API Proyecto Final funcionando"}

