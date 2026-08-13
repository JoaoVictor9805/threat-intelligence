from app.schemas.indicatorResponse import (
    IndicatorResponse,
    ValidationResponse,
    FalsePositiveResponse,
    PulseResponse
)

def transformar_resposta_otx(dados: dict) -> IndicatorResponse:

    # Validações
    validations = [
        ValidationResponse(**item)
        for item in dados.get("validation", [])
    ]

    # Falsos positivos
    false_positives = [
        FalsePositiveResponse(**item)
        for item in dados.get("false_positive", [])
    ]

    # Pulses
    pulses = [
        PulseResponse(
            id=pulse["id"],
            name=pulse["name"],
            description=pulse["description"],
            modified=pulse["modified"],
            created=pulse["created"],
            tags=pulse["tags"],
            references=pulse["references"],
            adversary=pulse["adversary"],
            targeted_countries=pulse["targeted_countries"],
            malware_families=pulse["malware_families"],
            attack_ids=pulse["attack_ids"],
            industries=pulse["industries"],
            tlp=pulse["TLP"]
        )
        for pulse in dados.get("pulse_info", {}).get("pulses", [])
    ]

    # Resposta final
    return IndicatorResponse(
        indicador=dados["indicator"],
        tipo=dados["type"],
        reputacao=dados["reputation"],
        quantidade_pulses=dados.get("pulse_info", {}).get("count", 0),
        pulses=pulses,
        validation=validations,
        false_positive=false_positives
    )