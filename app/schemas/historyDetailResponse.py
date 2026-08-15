from datetime import datetime

from pydantic import BaseModel

from app.schemas.indicatorResponse import IndicatorResponse


class HistoryDetailResponse(BaseModel):

    # Informações da consulta armazenada no histórico
    id: int
    indicador: str
    tipo: str
    fonte: str
    dataConsulta: datetime
    resumoIa: str | None = None

    # Resultado da análise realizada na época da consulta
    resultado: IndicatorResponse