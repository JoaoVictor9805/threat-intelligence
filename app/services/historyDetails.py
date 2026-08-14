from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.consultation import Consultation
from app.schemas.historyDetailResponse import HistoryDetailResponse
from app.schemas.indicatorResponse import IndicatorResponse


def carregar_consulta_detalhada(
    db: Session,
    id: int
) -> HistoryDetailResponse | None:

    consulta = db.scalar(
        select(Consultation)
        .where(Consultation.id == id)
    )

    if consulta is None:
        return None

    resultado = IndicatorResponse(
        **consulta.resultado
    )

    return HistoryDetailResponse(
        id=consulta.id,
        indicador=consulta.indicador,
        tipo=consulta.tipo,
        fonte=consulta.fonte,
        dataConsulta=consulta.dataConsulta,
        resultado=resultado
    )