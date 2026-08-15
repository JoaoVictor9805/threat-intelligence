from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.consultation import Consultation


def carregar_consultas(db: Session):            # "Quero fazer um SELECT utilizando a tabela representada pelo model Consultation."

    data_limite = datetime.now() - timedelta(days=30)

    consulta = (
        select(
            Consultation.id,
            Consultation.indicador,
            Consultation.tipo,
            Consultation.fonte,
            Consultation.dataConsulta
        )                                                        # Só as colunas que a listagem realmente usa
        .where(Consultation.dataConsulta >= data_limite)
        .order_by(Consultation.dataConsulta.desc())
    )

    resultado = db.execute(consulta).all()          # Linhas leves, sem o JSON pesado e sem o resumo_ia

    return resultado