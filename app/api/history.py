from pathlib import Path

from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates

from app.database.connection import SessionLocal
from app.services.historyLoad import carregar_consultas
from app.services.historyDetails import carregar_consulta_detalhada


router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


@router.get("/history")
def carregar_historico(request: Request):

    db = SessionLocal()

    try:
        consultas = carregar_consultas(db)

        return templates.TemplateResponse(
            request=request,
            name="history.html",
            context={
                "consultas": consultas
            }
        )

    finally:
        db.close()



@router.get("/history/details/{id}")
def carregar_detalhes_consulta(id: int):

    db = SessionLocal()

    try:
        resultado = carregar_consulta_detalhada(
            db,
            id
        )

        if resultado is None:
            raise HTTPException(
                status_code=404,
                detail="Consulta não encontrada."
            )

        return resultado

    finally:
        db.close()