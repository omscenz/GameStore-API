# archivo: utils/jwt_example.py
import jwt
import os
from datetime import datetime, timedelta

# Clave secreta de al menos 32 caracteres (256 bits)
SECRET_KEY = os.getenv("JWT_SECRET", "mi_clave_segura_muy_larga_1234567890")
ALGORITHM = "HS256"

def create_jwt_token(user_id: str, name: str, email: str, admin: bool = False) -> str:
    payload = {
        "sub": user_id,               # ID del usuario
        "name": name,
        "email": email,
        "admin": admin,
        "exp": datetime.utcnow() + timedelta(hours=1)  # Expira en 1 hora
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

# Ejemplo de uso
if __name__ == "__main__":
    token = create_jwt_token("123456", "Orlin", "orlin@example.com", True)
    print("JWT generado:", token)
