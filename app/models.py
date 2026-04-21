from typing import Optional
from pydantic import BaseModel, Field


class FechaModel(BaseModel):
    dia: Optional[str] = None
    mes: Optional[str] = None
    anio: Optional[str] = None


class CursoModel(BaseModel):
    tipo: Optional[str] = None
    c1: Optional[int] = None
    c2: Optional[int] = None
    c3: Optional[int] = None


class HojaDeResolucionResponse(BaseModel):
    dni: Optional[str] = None
    fecha: FechaModel
    curso: CursoModel
    respuestas: dict[str, Optional[str]]
    warnings: list[str] = Field(default_factory=list)
