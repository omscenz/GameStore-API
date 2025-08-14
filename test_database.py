import pytest
from utils.mongodb import t_connection, t_connection, get_collection, get_mongo_client
import os
from dotenv import load_dotenv

load_dotenv()

def test_env_variables():
   mongodb_uri = os.getenv("ATLAS_URI")

   assert mongodb_uri is not None, "La variable de entorno 'ATLAS_URI' no está definida"
   print(f"Database': {mongodb_uri}")


def test_mongo_client():
    try:
        client = get_mongo_client()
        assert client is not None, "El cliente de Mongo is Nones"
    except Exception as e:
        pytest.fail(f"Error en el llamado del cliente: {e}")


def test_connect():
   try:
       connection_result = t_connection()
       assert connection_result is True, "La conexion a la base de datos fallo"
   except Exception as e:
          pytest.fail(f"Error en la conexion a MongoDB: {e}")

def test_get_collection():
    try:
        coll_users = get_collection("users")
        assert coll_users is not None, "Error al obtener la collection de users"
    except Exception as e:
        pytest.fail(f"Error al obtener la coleccion 'users': {e}")