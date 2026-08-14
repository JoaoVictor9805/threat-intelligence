from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.consultation import Consultation


def carregar_consultas(db: Session):            # "Quero fazer um SELECT utilizando a tabela representada pelo model Consultation."

    data_limite = datetime.now() - timedelta(days=30)

    consulta = (
        select(Consultation)                                    # "Ordene pelo campo dataConsulta, do maior para o menor."
        .where(Consultation.dataConsulta >= data_limite)
        .order_by(Consultation.dataConsulta.desc())
    )

    resultado = db.scalars(consulta).all()          # Recebemos objetos do seu model:

    return resultado