import os                           # O os é um módulo da biblioteca padrão do Python que permite interagir com funcionalidades do sistema operacional
import httpx                        # É uma biblioteca Python para realizar requisições HTTP
from dotenv import load_dotenv      # Carregar arquivo .env
from urllib.parse import quote

load_dotenv()


otx_base_url = "https://otx.alienvault.com/api/v1"
api_key = os.getenv("OTX_API_KEY")                                      # "Pegue o valor de uma variável de ambiente."


def consultar_indicador(tipo: str, indicator: str):
    tipos_otx = {
        "IPv4": "IPv4",
        "md5": "file",
        "sha1": "file",
        "sha256": "file",
        "url": "url"
    }

    tipo_otx = tipos_otx[tipo]

    indicator_codificado = quote(indicator, safe="")
    url = f"{otx_base_url}/indicators/{tipo_otx}/{indicator_codificado}/general"

    headers = {
        "X-OTX-API-KEY": api_key                                            # é o nome do header que a OTX espera para autenticação.
    }

    try: 
        response = httpx.get(
            url, 
            headers=headers,
            timeout=10.0
        )

        response.raise_for_status()

        return response.json()
    
    except httpx.HTTPStatusError as erro:
        raise RuntimeError(f"OTX retornou o status {erro.response.status_code}") # conseguimos falar com a OTX mas ela respondeu com erro


    except httpx.RequestError:
        raise RuntimeError("Não foi possível conectar à API OTX.") # não conseguimos completar a comunicação com a OTX