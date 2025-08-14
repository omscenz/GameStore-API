from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
ATLAS_URI = os.getenv("ATLAS_URI")

if not ATLAS_URI:
    raise Exception("La variable de entorno ATLAS_URI no está configurada")

if not DB_NAME:
    raise Exception("La variable de entorno DB_NAME no está configurada")

# Crear cliente asíncrono para MongoDB Atlas
client = AsyncIOMotorClient(ATLAS_URI)
db = client[DB_NAME]

def get_collection(name: str):
    """
    Retorna la colección MongoDB con el nombre dado.
    """
    return db[name]
