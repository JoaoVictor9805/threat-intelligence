from sqlalchemy.orm import Session

from app.models.consultation import Consultation
from app.schemas.indicatorResponse import IndicatorResponse


def salvar_consulta(
    db: Session,
    resultado: IndicatorResponse
):
    consulta = Consultation(
        indicador=resultado.indicador,
        tipo=identificar_tipo_banco(resultado.tipo),
        fonte="OTX",
        resultado=resultado.model_dump(mode="json") #Converte do tipo IndicatorResponse para JSON para armazenar adequadamente no BD
    )

    db.add(consulta)
    db.commit()
    db.refresh(consulta)

    return consulta


def identificar_tipo_banco(tipo: str) -> str:

    if tipo == "IPv4":
        return "ip"

    if tipo in ("URL", "domain", "hostname", "url"):
        return "dominio"

    if tipo in ("MD5", "SHA1", "SHA256", "md5", "sha1", "sha256"):
        return "hash"

    raise ValueError(f"Tipo de indicador não suportado: {tipo}")


def salvar_resumo_ia(
    db: Session,
    consulta_id: int,
    resumo: str
):
    consulta = db.get(Consultation, consulta_id)

    if consulta is None:
        raise ValueError(f"Consulta {consulta_id} não encontrada.")

    consulta.resumoIa = resumo

    db.commit()