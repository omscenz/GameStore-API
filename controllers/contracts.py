from fastapi import HTTPException
from bson import ObjectId
from models.contracts import Contract
from utils.mongodb import get_collection

contracts_collection = get_collection("contracts")  # Colección principal
contract_types_collection = get_collection("contract_types")  # Colección de tipos

async def create_contract(item: Contract):
    # Validar ID del tipo de contrato
    if not ObjectId.is_valid(item.type_contract_id):
        raise HTTPException(status_code=400, detail=f"ID de tipo inválido: {item.type_contract_id}")

    # Verificar que el tipo de contrato existe y está activo
    tipo = await contract_types_collection.find_one({"_id": ObjectId(item.type_contract_id), "active": True})
    if not tipo:
        raise HTTPException(status_code=400, detail="Tipo no válido o inactivo")

    # Insertar documento
    item_dict = item.model_dump(exclude_unset=True)
    result = await contracts_collection.insert_one(item_dict)
    item.id = str(result.inserted_id)
    return item

async def list_contracts(skip: int = 0, limit: int = 10):
    cursor = contracts_collection.find({"active": True}).skip(skip).limit(limit)
    items = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        items.append(Contract(**doc))
    total = await contracts_collection.count_documents({"active": True})
    return {
        "items": items,
        "total": total,
        "skip": skip,
        "limit": limit
    }

async def get_contract_by_id(item_id: str):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    doc = await contracts_collection.find_one({"_id": ObjectId(item_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return Contract(**doc)

async def update_contract(item_id: str, item_data: dict):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    # Validar nuevo tipo si se incluye en los datos
    if "type_contract_id" in item_data:
        if not ObjectId.is_valid(item_data["type_contract_id"]):
            raise HTTPException(status_code=400, detail="ID de tipo inválido")
        tipo = await contract_types_collection.find_one({"_id": ObjectId(item_data["type_contract_id"]), "active": True})
        if not tipo:
            raise HTTPException(status_code=400, detail="Tipo no válido o inactivo")

    result = await contracts_collection.update_one({"_id": ObjectId(item_id)}, {"$set": item_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return {"message": "Registro actualizado correctamente"}

async def delete_contract(item_id: str):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="ID inválido")
    result = await contracts_collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return {"message": "Registro eliminado correctamente"}

async def disable_contract(item_id: str):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    result = await contracts_collection.update_one(
        {"_id": ObjectId(item_id)},
        {"$set": {"active": False}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Contrato no encontrado")

    return {"message": "Contrato desactivado correctamente"}

