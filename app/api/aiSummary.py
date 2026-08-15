from fastapi import APIRouter, HTTPException

from app.schemas.indicatorResponse import IndicatorResponse
from app.schemas.aiSummaryResponse import AISummaryResponse
from app.services.aiSummary import gerar_resumo_ia


router = APIRouter()


@router.post(
    "/ai/summary",
    response_model=AISummaryResponse
)
def gerar_resumo(resultado: IndicatorResponse):

    print(">>> ENTROU NO /ai/summary")
    print(">>> RESULTADO:", resultado)

    try:

        resumo = gerar_resumo_ia(resultado)

        print(">>> RESUMO GERADO:", resumo)

        return AISummaryResponse(
            resumo=resumo
        )

    except Exception as erro:

        print(">>> ERRO NA IA:", repr(erro))

        raise HTTPException(
            status_code=502,
            detail="Não foi possível gerar o resumo por IA."
        )