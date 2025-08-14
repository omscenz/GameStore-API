from fastapi import APIRouter, Body
from models.login import Login

router = APIRouter(tags=["Login"])

@router.post("/login")
def login(credentials: Login = Body(...)):
    # Ahora puedes acceder a email y password
    return {
        "mensaje": "Usuario autenticado correctamente",
        "email": credentials.email,
        "password": credentials.password  # normalmente no se devuelve
    }
