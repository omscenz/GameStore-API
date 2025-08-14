from fastapi import APIRouter, Depends, Header, HTTPException, Body
from typing import Optional, List

from controllers import users as user_controller
from models.users import User
from models.login import Login
from utils.security import verify_firebase_token

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Crear usuario (registro en tu DB, Firebase maneja auth)
@router.post("", response_model=User)
async def register_user(user: User):
    return await user_controller.create_user(user)

# Listar todos los usuarios (solo admin)
@router.get("", response_model=List[User])
async def get_all_users(authorization: Optional[str] = Header(None)):
    payload = verify_firebase_token(authorization)
    if not payload.get("admin"):
        raise HTTPException(status_code=403, detail="Permisos insuficientes")
    return await user_controller.list_users()

# Obtener usuario por ID (solo admin)
@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str, authorization: Optional[str] = Header(None)):
    payload = verify_firebase_token(authorization)
    if not payload.get("admin"):
        raise HTTPException(status_code=403, detail="Permisos insuficientes")
    return await user_controller.get_user_by_id(user_id)

# Actualizar usuario (solo el mismo usuario o admin)
@router.put("/{user_id}", response_model=User)
async def update_user(user_id: str, user: User, authorization: Optional[str] = Header(None)):
    payload = verify_firebase_token(authorization)
    if not payload.get("admin") and payload.get("uid") != user_id:
        raise HTTPException(status_code=403, detail="Solo puedes editar tu propia cuenta")
    return await user_controller.update_user(user_id, user)

# Desactivar usuario (solo admin)
@router.delete("/{user_id}")
async def deactivate_user(user_id: str, authorization: Optional[str] = Header(None)):
    payload = verify_firebase_token(authorization)
    if not payload.get("admin"):
        raise HTTPException(status_code=403, detail="Permisos insuficientes")
    return await user_controller.deactivate_user(user_id)


# ----- Login fuera del prefijo /users -----
login_router = APIRouter(
    prefix="/login",
    tags=["Login"]
)

@login_router.post("")
async def login_user(user: Login = Body(...)):
    return await user_controller.login(user)
