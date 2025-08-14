from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Cargar variables de entorno desde .env
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
ATLAS_URI = os.getenv("ATLAS_URI")

if not ATLAS_URI:
    raise Exception("La variable de entorno ATLAS_URI no está configurada")

if not DB_NAME:
    raise Exception("La variable de entorno DB_NAME no está configurada")


client = AsyncIOMotorClient(ATLAS_URI)
db = client[DB_NAME]

def get_collection(name: str):
    """
    Retorna la colección MongoDB con el nombre dado.
    """
    return db[name]

def t_connection():
        try:
            client = get_mongo_client()
            client.admin.command("ping")
            return True
        except Exception as e:
            print(f"Error conectando a MongoDB: {e}")
            return False

def get_mongo_client():
    "Obtiene el cliente de MongoDB"
    global client
    if client is None:
        client = MongoClient(
                ATLAS_URI,
                server_api=ServerApi("1"),
                tls=True,
                tlsAllowInvalidCertificates=True,
                serverSelectionTimeoutMS=5000

        )
    return client

  
