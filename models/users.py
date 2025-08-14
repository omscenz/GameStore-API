from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="MongoDB ID - Generado automáticamente desde el _id de MongoDB, no es necesario enviarlo en POST"
    )

    firebase_uid: Optional[str] = Field(
        default=None,
        description="UID generado por Firebase Authentication"
    )

    name: str = Field(
        description="Nombre visible del usuario en la plataforma",
        min_length=3,
        max_length=50,
        pattern=r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9' _-]+$",
        examples=["GamerMaster123", "Ana_López"]
    )

    email: str = Field(
        description="Correo electrónico del usuario",
        pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        examples=["usuario@example.com"]
    )

    date_birth: Optional[str] = Field(   
        default=None,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="Fecha de nacimiento en formato YYYY-MM-DD",
        examples=["2000-05-30"]
    )

    active: bool = Field(
        default=True,
        description="Estado activo del usuario"
    )

    admin: bool = Field(
        default=False,
        description="Rol administrador del sistema"
    )

    password: str = Field(
        min_length=8,
        max_length=64,
        description="Contraseña segura. Mínimo 8 caracteres, incluyendo una mayúscula, un número y un carácter especial.",
        examples=["Password123!"]
    )

__all__ = ["User"]
