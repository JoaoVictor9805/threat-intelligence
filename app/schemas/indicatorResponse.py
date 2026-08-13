from pydantic import BaseModel
from datetime import datetime

class ValidationResponse(BaseModel):
    source: str                  # Origem da validação ou mecanismo que gerou a informação
    message: str                 # Mensagem descritiva da validação
    name: str                    # Nome/título da validação


class FalsePositiveResponse(BaseModel):
    assessment: str                   # Resultado/avaliação atribuída ao possível falso positivo
    assessment_date: datetime         # Data em que a avaliação do falso positivo foi realizada
    report_date: datetime             # Data em que o falso positivo foi reportado

class MalwareFamilyResponse(BaseModel):
    id: str
    display_name: str
    target: str | None = None

class PulseResponse(BaseModel):
    id: str                              # Identificador único do Pulse
    name: str                            # Nome/título do Pulse
    description: str                     # Descrição da ameaça ou campanha
    modified: datetime                  # Data da última modificação do Pulse
    created: datetime                    # Data de criação do Pulse
    tags: list[str]                      # Tags associadas ao Pulse
    references: list[str]                # Referências utilizadas no Pulse
    adversary: str                       # Adversário/grupo associado
    targeted_countries: list[str]        # Países potencialmente alvos
    malware_families: list[MalwareFamilyResponse]
    attack_ids: list[dict]               # Técnicas/táticas MITRE ATT&CK relacionadas
    industries: list[str]                # Setores potencialmente afetados
    tlp: str                             # Classificação de compartilhamento (Traffic Light Protocol)

class IndicatorResponse(BaseModel):

    # Identificação
    indicador: str               # Indicador consultado (IP, URL ou hash)
    tipo: str                    # Tipo do indicador (IPv4, URL, MD5, SHA1 ou SHA256)

    # Reputação / ameaça
    reputacao: int                                  # Pontuação de reputação atribuída pela OTX
    quantidade_pulses: int                          # Quantidade de Pulses relacionados ao indicador
    pulses: list[PulseResponse]                     # Pulses que fornecem contexto sobre ameaças relacionadas ao indicador
    validation: list[ValidationResponse]            # Lista de validações/alertas relacionados ao indicador
    false_positive: list[FalsePositiveResponse]     # Lista de avaliações de possíveis falsos positivos

    # Localização
    pais: str | None = None                  # Nome do país associado ao indicador
    codigo_pais: str | None = None           # Código do país associado ao indicador
    continente: str | None = None            # Código do continente associado ao indicador
    cidade: str | None = None                # Cidade associada ao indicador
    regiao: str | None = None                # Região associada ao indicador
    subdivisao: str | None = None            # Subdivisão administrativa, como estado ou província

    # Infraestrutura
    asn: str | None = None                   # Autonomous System Number associado ao indicador
    whois: str | None = None                 # Endereço para consulta das informações WHOIS do indicador


    # Uma resposta (IndicatorResponse) que é composta por vários tipos de informação, alguns dos quais possuem estruturas próprias (ValidationResponse e FalsePositiveResponse).