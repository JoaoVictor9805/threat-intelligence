from fastapi import APIRouter       # nos permite criar um "grupo de rotas".
from fastapi import HTTPException, Response
from pydantic import ValidationError
from fastapi.responses import FileResponse
from pathlib import Path

from app.schemas.indicatorRequest import IndicatorRequest      # Validação do dado digitado pelo usuário e definição do tipo
from app.services.otx import consultar_indicador        # Consulta o indicador na api AlienWare OTX
from app.services.indicatorMapper import transformar_resposta_otx

from app.database.connection import SessionLocal
from app.services.historySave import salvar_consulta

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent

@router.get("/indicators")
def pagina_indicators():
    return FileResponse(BASE_DIR / "templates" / "index.html")


@router.get("/indicators/{indicator:path}")
def receber_parametros(indicator: str, response: Response):

    try: 
        dados = IndicatorRequest(indicator=indicator)

    except ValidationError as erro:

            mensagem = erro.errors()[0]["msg"]

            raise HTTPException(
                status_code=400,
                detail=mensagem
            )
    
    try:
        resultado_otx = consultar_indicador(
            dados.tipo,
            dados.indicator
        )

        resultado = transformar_resposta_otx(resultado_otx)

        db = SessionLocal()

        try:
            consulta = salvar_consulta(
            db,
            resultado
            )

            response.headers["X-Consulta-Id"] = str(consulta.id)

        finally:
            db.close()

        return resultado
    
    except RuntimeError as erro:

        raise HTTPException(
            status_code=502,        # Porque seu servidor está funcionando, mas um serviço externo que ele depende apresentou problema.
            detail=str(erro)        # o RuntimeError é apenas a forma como o nosso código repassa esses problemas para outra camada, evitando expor detalhes desnecessários sobre o problema
                                    # Ideal apontar tipo de erro específico aqui em um versionamento posterior
        )

