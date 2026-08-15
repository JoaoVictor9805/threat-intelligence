from app.schemas.indicatorResponse import (
    IndicatorResponse,
    ValidationResponse,
    FalsePositiveResponse,
    PulseResponse
)


def transformar_resposta_otx(dados: dict) -> IndicatorResponse:

    # ============================================================
    # VALIDAÇÕES
    # ============================================================

    validations = [
        ValidationResponse(**item)
        for item in dados.get("validation", [])
    ]


    # ============================================================
    # FALSOS POSITIVOS
    # ============================================================

    false_positives = [
        FalsePositiveResponse(**item)
        for item in dados.get("false_positive", [])
    ]


    # ============================================================
    # PULSES
    # ============================================================

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
        for pulse in dados.get(
            "pulse_info",
            {}
        ).get(
            "pulses",
            []
        )
    ]


    # ============================================================
    # RESPOSTA FINAL
    # ============================================================

    return IndicatorResponse(

        # --------------------------------------------------------
        # Identificação
        # --------------------------------------------------------

        indicador=dados["indicator"],

        tipo=dados["type"],


        # --------------------------------------------------------
        # Reputação / ameaça
        # --------------------------------------------------------

        reputacao=dados["reputation"],

        quantidade_pulses=
            dados.get(
                "pulse_info",
                {}
            ).get(
                "count",
                0
            ),

        pulses=pulses,

        validation=validations,

        false_positive=false_positives,


        # --------------------------------------------------------
        # Localização
        # --------------------------------------------------------

        pais=dados.get("country_name"),

        codigo_pais=dados.get("country_code"),

        continente=dados.get("continent_code"),

        cidade=dados.get("city"),

        regiao=dados.get("region"),

        subdivisao=dados.get("subdivision"),


        # --------------------------------------------------------
        # Infraestrutura
        # --------------------------------------------------------

        asn=dados.get("asn"),

        whois=dados.get("whois")
    )