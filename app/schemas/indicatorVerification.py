from pydantic import BaseModel          # É a classe base do Pydantic usada para criar nossos modelos de dados. Essa classe representa dados que precisam ser analisados, validados e convertidos conforme as regras que definirmos."
from pydantic import model_validator    # É uma ferramenta do Pydantic para criar uma regra de validação para um model completo.

import ipaddress
import re
from urllib.parse import urlparse

class IndicatorRequest(BaseModel):
    indicator: str
    tipo: str = ""

    @model_validator(mode="after")      # Nesse modo, o modelo já foi construído e o validator recebe a própria instância:
    def validar_indicator(self): 

        self.indicator = self.indicator.strip()

         # 1. Verifica se está vazio
        if not self.indicator:
            raise ValueError("O indicador não pode estar vazio.")


        # 2. Verifica se é IPv4 válido
        try:
            ip = ipaddress.ip_address(self.indicator)

            if isinstance(ip, ipaddress.IPv4Address):
                self.tipo = "IPv4"
                return self
            
        except ValueError:
            pass


        # 3. Verifica se é um hash
        if re.fullmatch(r"[a-fA-F0-9]{32}", self.indicator):
            self.tipo = "md5"
            return self

        if re.fullmatch(r"[a-fA-F0-9]{40}", self.indicator):
            self.tipo = "sha1"
            return self

        if re.fullmatch(r"[a-fA-F0-9]{64}", self.indicator):
            self.tipo = "sha256"
            return self


        # 4. Verifica se é uma URL
        try:
            resultado = urlparse(self.indicator)                                         # urlparse() serve para separar uma URL em suas partes.

            if resultado.scheme in ("http", "https") and resultado.netloc:      # 1. É HTTP ou HTTPS? e 2. Existe um endereço/domínio?
                self.tipo = "url"
                return self
            
        except ValueError:
            pass


        # 5. Se não passou em nenhuma validação
        raise ValueError(
            "Indicador inválido. Informe um IPv4, uma URL ou um hash válido."
        )