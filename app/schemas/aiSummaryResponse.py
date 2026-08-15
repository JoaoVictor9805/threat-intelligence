from pydantic import BaseModel


class AISummaryResponse(BaseModel):
    resumo: str