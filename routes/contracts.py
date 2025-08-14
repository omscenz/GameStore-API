from fastapi import APIRouter, Path, Body, Query, status, Request
from typing import List
from models.contracts import Contract
from controllers.contracts import (
    create_contract,
    list_contracts,
    get_contract_by_id,
    update_contract,
    disable_contract,
   # create_contract_with_validation
)
from utils.security import validateadmin, validateuser

router = APIRouter(prefix="/contracts", tags=["Contracts"])

@router.post(
    "",
    summary="Crear un nuevo contrato",
    response_model=Contract,
    status_code=status.HTTP_201_CREATED
)
@validateadmin
async def add_contract(contract: Contract):
    return await create_contract(contract)

@router.get(
    "",
    summary="Listar contratos activos con paginación",
    response_model=dict
)
@validateadmin
async def get_contracts(skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100)):
    return await list_contracts(skip, limit)

@router.get(
    "/{contract_id}",
    summary="Obtener contrato por ID",
    response_model=Contract
)
@validateadmin
async def get_contract(contract_id: str = Path(..., description="ID del contrato")):
    return await get_contract_by_id(contract_id)

@router.put(
    "/{contract_id}",
    summary="Actualizar un contrato"
)
@validateadmin
async def edit_contract(contract_id: str, contract_data: dict = Body(...)):
    return await update_contract(contract_id, contract_data)

@router.delete(
    "/{contract_id}",
    summary="Desactivar (no eliminar) un contrato"
)
@validateadmin
async def remove_contract(contract_id: str):
    return await disable_contract(contract_id)

#@router.post("/validated", summary="Crear contrato con validación compleja")
#@validateadmin
#async def create_validated_contract(contract: Contract):
#    return await create_contract_with_validation(contract)
