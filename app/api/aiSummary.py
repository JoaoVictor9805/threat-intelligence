from fastapi import APIRouter, HTTPException

from app.schemas.indicatorResponse import IndicatorResponse
from app.schemas.aiSummaryResponse import AISummaryResponse
from app.services.aiSummary import gerar_resumo_ia
from app.database.connection import SessionLocal
from app.services.historySave import salvar_resumo_ia

router = APIRouter()


@router.post(
    "/ai/summary",
    response_model=AISummaryResponse
)

def gerar_resumo(resultado: IndicatorResponse, consulta_id: int):

    try:

        resumo = gerar_resumo_ia(resultado)

        db = SessionLocal()

        try:
            salvar_resumo_ia(db, consulta_id, resumo)

        except Exception as erro_db:

            print(">>> ERRO AO SALVAR RESUMO NO BANCO:", repr(erro_db))
            # não relança — o resumo já foi gerado e vai ser mostrado
            # ao usuário mesmo que o salvamento falhe

        finally:
            db.close()

        return AISummaryResponse(
            resumo=resumo
        )

    except Exception as erro:

        raise HTTPException(
            status_code=502,
            detail="Não foi possível gerar o resumo por IA."
        )