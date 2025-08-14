import os
import logging
import firebase_admin
import requests
from fastapi import HTTPException, status
from firebase_admin import credentials, auth as firebase_auth
from bson import ObjectId

from models.users import User
from models.login import Login
from utils.security import create_jwt_token
from utils.mongodb import get_collection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar Firebase con ruta desde .env
if not firebase_admin._apps:
    firebase_cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
    if not firebase_cred_path or not os.path.exists(firebase_cred_path):
        raise Exception("La variable FIREBASE_CREDENTIALS_PATH no está configurada o el archivo no existe")

    cred = credentials.Certificate(firebase_cred_path)
    firebase_admin.initialize_app(cred)

# Crear usuario
async def create_user(user: User) -> User:
    try:
        user_record = firebase_auth.create_user(
            email=user.email,
            password=user.password
        )
    except Exception as e:
        logger.warning(e)
        raise HTTPException(status_code=400, detail="Error al registrar usuario en Firebase")

    try:
        coll = get_collection("users")

        new_user = User(
            name=user.name,
          #  lastname=user.lastname,
            email=user.email,
            password=user.password
        )

        user_dict = new_user.model_dump(exclude={"id", "password"})
        result = await coll.insert_one(user_dict)
        new_user.id = str(result.inserted_id)
        new_user.password = "*********"  # Enmascarar

        return new_user

    except Exception as e:
        firebase_auth.delete_user(user_record.uid)
        logger.error(f"Error creando usuario en MongoDB: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en base de datos")

# Login
async def login(user: Login) -> dict:
    api_key = os.getenv("FIREBASE_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="FIREBASE_API_KEY no está definida")

    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    payload = {
        "email": user.email,
        "password": user.password,
        "returnSecureToken": True
    }

    response = requests.post(url, json=payload)
    response_data = response.json()

    if "error" in response_data:
        raise HTTPException(status_code=400, detail="Error al autenticar usuario")

    coll = get_collection("users")
    user_info = await coll.find_one({"email": user.email})

    if not user_info:
        raise HTTPException(status_code=404, detail="Usuario no encontrado en la base de datos")

    return {
        "message": "Usuario autenticado correctamente",
        "idToken": create_jwt_token(
            user_info["name"],
            #user_info["lastname"],
            user_info["email"],
            user_info.get("active", True),
            user_info.get("admin", False),
             str(user_info["_id"])
        )
    }

# Listar usuarios
async def list_users():
    coll = get_collection("users")
    docs = await coll.find().to_list(None)
    for doc in docs:
        doc["id"] = str(doc["_id"])
        doc.pop("_id", None)
        doc.pop("password", None)
    return docs

# Obtener usuario por ID
async def get_user_by_id(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    coll = get_collection("users")
    doc = await coll.find_one({"_id": ObjectId(user_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    doc["id"] = str(doc["_id"])
    doc.pop("_id", None)
    doc.pop("password", None)
    return doc

# Actualizar usuario
async def update_user(user_id: str, user: User):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    coll = get_collection("users")
    update_data = user.model_dump(exclude_unset=True, exclude={"id", "password"})
    result = await coll.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    updated_doc = await coll.find_one({"_id": ObjectId(user_id)})
    updated_doc["id"] = str(updated_doc["_id"])
    updated_doc.pop("_id", None)
    updated_doc.pop("password", None)
    return updated_doc

# Desactivar usuario
async def deactivate_user(user_id: str):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    coll = get_collection("users")
    result = await coll.update_one({"_id": ObjectId(user_id)}, {"$set": {"active": False}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"message": "Usuario desactivado correctamente"}
