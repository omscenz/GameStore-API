# utils/security.py
import firebase_admin
from firebase_admin import auth, credentials
from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from functools import wraps
from typing import Optional
import jwt
import os
from datetime import datetime, timedelta

# Inicializar Firebase solo una vez
if not firebase_admin._apps:
    cred = credentials.Certificate("secrets/firebase_credentials.json")
    firebase_admin.initialize_app(cred)

security = HTTPBearer()

def verify_firebase_token(token: Optional[str]) -> dict:
    if not token:
        raise HTTPException(status_code=401, detail="Token requerido")

    try:
        if token.startswith("Bearer "):
            token = token.split(" ")[1]

        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")


# Decoradores estilo original pero usando Firebase
def validateuser(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get('request')
        if not request:
            raise HTTPException(status_code=400, detail="Request object not found")

        token = request.headers.get("Authorization")
        decoded_token = verify_firebase_token(token)

        if not decoded_token.get("email_verified", True):
            raise HTTPException(status_code=401, detail="Email no verificado")

        request.state.uid = decoded_token["uid"]
        request.state.email = decoded_token.get("email")
        request.state.name_profile = decoded_token.get("name_profile")

        return await func(*args, **kwargs)
    return wrapper


def validateadmin(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get('request')
        if not request:
            raise HTTPException(status_code=400, detail="Request object not found")

        token = request.headers.get("Authorization")
        decoded_token = verify_firebase_token(token)

        # Aquí admin sería un "custom claim" en Firebase
        if not decoded_token.get("admin", False):
            raise HTTPException(status_code=403, detail="No tienes permisos de administrador")

        request.state.uid = decoded_token["uid"]
        request.state.email = decoded_token.get("email")
        request.state.name_profile = decoded_token.get("name_profile")
        request.state.admin = True

        return await func(*args, **kwargs)
    return wrapper


# Dependencias FastAPI
def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    decoded_token = verify_firebase_token(credentials.credentials)
    return decoded_token

def validate_admin(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    decoded_token = verify_firebase_token(credentials.credentials)
    if not decoded_token.get("admin", False):
        raise HTTPException(status_code=403, detail="No tienes permisos de administrador")
    return decoded_token



SECRET_KEY = os.getenv("SECRET_KEY", "defaultsecret")
ALGORITHM = "HS256"

def create_jwt_token(name: str, email: str, active: bool, admin: bool, user_id: str) -> str:
    SECRET_KEY = os.getenv("SECRET_KEY", "mi_clave_secreta")
    payload = {
        "sub": user_id,
        "name": name,
        "email": email,
        "active": active,
        "admin": admin,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


__all__ = [
    "validateuser",
    "validateadmin",
    "validate_token",
    "validate_admin",
    "create_jwt_token"
]
