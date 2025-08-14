from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from bson import ObjectId
from utils.pyobjectid import PyObjectId

class Contract(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id", description="ID generado automáticamente")
    developer_id: PyObjectId = Field(..., description="ID del desarrollador que firma el contrato")
    game_id: PyObjectId = Field(..., description="ID del juego asociado al contrato")
    type_contract_id: PyObjectId = Field(..., description="ID del tipo de contrato")
    start_date: date = Field(..., description="Fecha de inicio del contrato")
    end_date: Optional[date] = Field(None, description="Fecha final del contrato (opcional)")
    active: bool = Field(default=True, description="Estado activo/inactivo del contrato")

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }

# Modelo para respuestas paginadas
class ContractPaginatedResponse(BaseModel):
    total: int
    page: int
    page_size: int
    contracts: list[Contract]
