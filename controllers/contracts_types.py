from fastapi import HTTPException
from bson import ObjectId
from models.contracts_types import ContractType
from utils.mongodb import get_collection

types_collection = get_collection("types")  # Colección de Tipos
main_collection = get_collection("main_model")  # Colección del Modelo Principal

async def create_contract_type(tipo: ContractType):
    existing = await types_collection.find_one({
        "description": {
            "$regex": f"^{tipo.description}$",
            "$options": "i"
        }
    })
    if existing:
        raise HTTPException(status_code=400, detail="Este tipo ya existe")

    tipo_dict = tipo.model_dump(exclude_unset=True)
    result = await types_collection.insert_one(tipo_dict)
    tipo.id = str(result.inserted_id)
    return tipo

async def list_contract_types(skip: int = 0, limit: int = 10):
    cursor = types_collection.find({"active": True}).skip(skip).limit(limit)
    types_list = []
    async for t in cursor:
        t["id"] = str(t["_id"])
        types_list.append(t)

    total = await types_collection.count_documents({"active": True})
    return {
        "types": types_list,
        "total": total,
        "skip": skip,
        "limit": limit
    }

async def get_type_by_id(type_id: str):
    if not ObjectId.is_valid(type_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    t = await types_collection.find_one({"_id": ObjectId(type_id)})
    if not t:
        raise HTTPException(status_code=404, detail="Tipo no encontrado")

    t["id"] = str(t["_id"])
    return t

async def update_contract_type(type_id: str, type_data: dict):
    if not ObjectId.is_valid(type_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    existing = await types_collection.find_one({
        "description": {
            "$regex": f"^{type_data.get('description', '')}$",
            "$options": "i"
        },
        "_id": {"$ne": ObjectId(type_id)}
    })
    if existing:
        raise HTTPException(status_code=400, detail="Este tipo ya existe")

    result = await types_collection.update_one(
        {"_id": ObjectId(type_id)},
        {"$set": type_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Tipo no encontrado")

    return {"message": "Tipo actualizado correctamente"}

async def disable_contract_type(type_id: str):
    if not ObjectId.is_valid(type_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    # 🔹 Lógica de eliminación segura:
    associated_count = await main_collection.count_documents({"type_id": type_id})
    if associated_count > 0:
        # En vez de eliminar, desactivar
        await types_collection.update_one(
            {"_id": ObjectId(type_id)},
            {"$set": {"active": False}}
        )
        return {"message": "Tipo desactivado porque está en uso"}

    # Si no está en uso, eliminar permanentemente
    result = await types_collection.delete_one({"_id": ObjectId(type_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Tipo no encontrado")

    return {"message": "Tipo eliminado correctamente"}
