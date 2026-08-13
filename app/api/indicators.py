from fastapi import APIRouter       # nos permite criar um "grupo de rotas".
from fastapi import HTTPException
from pydantic import ValidationError

from app.schemas.indicatorVerification import IndicatorRequest      # Validação do dado digitado pelo usuário e definição do tipo
from app.services.otx import consultar_indicador        # Consulta o indicador na api AlienWare OTX

router = APIRouter()

@router.get("/indicators/{indicator}")
def receber_parametros(indicator: str):

    try: 
        dados = IndicatorRequest(indicator=indicator)

    except ValidationError as erro:

            mensagem = erro.errors()[0]["msg"]

            raise HTTPException(
                status_code=400,
                detail=mensagem
            )
    
    try:
        resultado = consultar_indicador(
            dados.tipo,
            dados.indicator
        )

        return resultado

    except RuntimeError as erro:

        raise HTTPException(
            status_code=502,        # Porque seu servidor está funcionando, mas um serviço externo que ele depende apresentou problema.
            detail=str(erro)        # o RuntimeError é apenas a forma como o nosso código repassa esses problemas para outra camada, evitando expor detalhes desnecessários sobre o problema
                                    # Ideal apontar tipo de erro específico aqui em um versionamento posterior
        )

