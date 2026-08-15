import os
import json

from google import genai
from google.genai import types

from dotenv import load_dotenv      # Carregar arquivo .env

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(
        timeout=10000  # 10000 ms = 10 segundos
    )
)


def gerar_resumo_ia(resultado) -> str:

    if hasattr(resultado, "model_dump"):
        dados = resultado.model_dump(mode="json")
    else:
        dados = resultado

    prompt = f"""
Você é um analista de Threat Intelligence.

Analise exclusivamente os dados fornecidos abaixo.

Não invente informações.
Não presuma informações que não estejam presentes.
Não atribua características ao indicador que não possam ser fundamentadas
pelos dados recebidos.

Gere um briefing curto, claro e compreensível para uma pessoa que não
possui conhecimento técnico profundo em Threat Intelligence.

O briefing deve, quando houver dados suficientes, abordar:

1. Identificação do indicador
2. Nível ou evidências de ameaça

O nível de ameaça deve ser descrito somente com base nas evidências
presentes nos dados recebidos. Não invente uma classificação de risco
nem transforme uma pontuação em "baixo", "médio" ou "alto" caso a
escala dessa pontuação não esteja explicitamente disponível.

Se houver Pulses, validações, famílias de malware, técnicas MITRE ATT&CK,
países-alvo ou outros dados relevantes, utilize-os para contextualizar
a ameaça.

Se esses dados estiverem ausentes ou vazios, informe essa limitação.

3. Principais informações encontradas
4. Possíveis riscos associados
5. Conclusão geral

Se não houver dados suficientes para uma conclusão confiável,
deixe isso explicitamente claro.

Não utilize símbolos de diagramação ".md" no seu resultado, trabalhe com formatações
diretas que não dependam de conversão

Dados da consulta:

{json.dumps(dados, ensure_ascii=False, indent=2)}
"""

    resposta = client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=prompt
    )

    return resposta.text