# Threat Intelligence Dashboard

Aplicação web para consulta e análise de indicadores de ameaça (IPs, URLs e hashes de arquivo), integrada à API pública **AlienVault OTX** e com geração opcional de resumos automáticos via **IA (Google Gemini)**. Todas as consultas realizadas ficam registradas em um histórico consultável, com dashboard interativo e gráficos.

> Status: MVP (produto mínimo viável) — funcionalidades principais implementadas e funcionais.

---

## Sumário

- [Funcionalidades](#funcionalidades)
- [Arquitetura e stack](#arquitetura-e-stack)
- [Gerenciamento do projeto](#gerenciamento-do-projeto)
- [Estrutura de pastas](#estrutura-de-pastas)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e configuração](#instalação-e-configuração)
- [Configuração do banco de dados](#configuração-do-banco-de-dados)
- [Variáveis de ambiente (.env)](#variáveis-de-ambiente-env)
- [Executando o projeto](#executando-o-projeto)
- [Como usar](#como-usar)
- [Capturas de tela](#capturas-de-tela)
- [Rotas da aplicação](#rotas-da-aplicação)
- [Fluxos de funcionamento (diagramas)](#fluxos-de-funcionamento-diagramas)
- [Limitações conhecidas / próximos passos](#limitações-conhecidas--próximos-passos)
- [Aviso sobre o processo de desenvolvimento](#aviso-sobre-o-processo-de-desenvolvimento)
---

## Funcionalidades

- **Consulta de indicadores de ameaça**: aceita IPv4, URLs (http/https) e hashes de arquivo (MD5, SHA1 ou SHA256), com detecção automática do tipo digitado.
- **Integração com a API OTX (AlienVault)**: busca reputação, Pulses (campanhas/ameaças relacionadas), validações, falsos positivos, localização e infraestrutura do indicador.
- **Dashboard visual**: KPIs, localização, infraestrutura, contexto de ameaça (malware families, técnicas MITRE ATT&CK, países-alvo, indústrias) e gráficos de barra (Chart.js).
- **Resumo com IA**: gera um briefing em linguagem simples a partir dos dados retornados pela OTX, usando a API do Google Gemini.
- **Histórico de consultas**: lista as consultas realizadas nos últimos 30 dias, com acesso aos detalhes completos de cada uma (incluindo o resumo de IA, se gerado).
- **Persistência em banco de dados**: toda consulta bem-sucedida é salva automaticamente em MySQL, incluindo o resultado completo em formato JSON.
- **Limpeza automática**: um evento agendado no próprio MySQL remove consultas com mais de 30 dias.

---

## Arquitetura e stack

| Camada | Tecnologia |
|---|---|
| Backend / API | [FastAPI](https://fastapi.tiangolo.com/) (Python) |
| ORM / Banco de dados | [SQLAlchemy](https://www.sqlalchemy.org/) + [MySQL](https://www.mysql.com/) (via `PyMySQL`) |
| Templates (SSR) | [Jinja2](https://jinja.palletsprojects.com/) |
| Frontend | HTML + JavaScript puro (vanilla) + [Chart.js](https://www.chartjs.org/) |
| Validação de dados | [Pydantic](https://docs.pydantic.dev/) |
| Cliente HTTP (chamadas externas) | [httpx](https://www.python-httpx.org/) |
| API externa de Threat Intel | [AlienVault OTX](https://otx.alienvault.com/) |
| API de IA | [Google Gemini](https://ai.google.dev/) (via `google-genai`) |
| Servidor ASGI | [Uvicorn](https://www.uvicorn.org/) |

A aplicação **não usa filas ou processamento em segundo plano** — cada requisição é tratada de forma síncrona, do recebimento até a resposta.

---

## Gerenciamento do projeto

O desenvolvimento foi organizado em um quadro no **Trello**, dividido em 3 sprints:

🔗 **[Acessar o quadro no Trello](https://trello.com/invite/b/6a7c7bfb4bed2bdfd145e139/ATTId57f7804c3c17b74077d33df045de4d181B95472/desafio-tecnico)**

| Sprint | Escopo |
|---|---|
| **Sprint 1** | Consulta de indicadores — integração com a API OTX, validação de entrada, mapeamento da resposta e dashboard inicial |
| **Sprint 2** | Histórico de consultas — listagem, persistência no banco de dados e tela de detalhes de cada consulta |
| **Sprint 3** | Resumo com IA — integração com a API do Google Gemini e geração de briefing automático |

---

## Estrutura de pastas

```
threat-intelligence/
├── app/
│   ├── main.py                     # ponto de entrada — registra as rotas (routers)
│   ├── api/                        # rotas / controllers
│   │   ├── indicators.py           # consulta de indicadores (OTX)
│   │   ├── history.py              # histórico e detalhes de consultas
│   │   └── aiSummary.py            # geração de resumo com IA
│   ├── services/                   # regras de negócio
│   │   ├── otx.py                  # integração com a API OTX
│   │   ├── indicatorMapper.py      # tradução do JSON da OTX para o schema interno
│   │   ├── historySave.py          # gravação no banco (consulta + resumo IA)
│   │   ├── historyLoad.py          # listagem do histórico
│   │   ├── historyDetails.py       # detalhes de uma consulta específica
│   │   └── aiSummary.py            # integração com a API do Gemini
│   ├── schemas/                    # contratos de dados (Pydantic)
│   │   ├── indicatorRequest.py
│   │   ├── indicatorResponse.py
│   │   ├── historyDetailResponse.py
│   │   └── aiSummaryResponse.py
│   ├── models/
│   │   └── consultation.py         # mapeamento ORM da tabela `consulta`
│   ├── database/
│   │   ├── connection.py           # configuração da engine/sessão SQLAlchemy
│   │   └── DB.sql                  # script de criação do banco/tabela/evento
│   ├── templates/                  # páginas HTML (Jinja2)
│   │   ├── index.html
│   │   ├── history.html
│   │   └── historyDetails.html
│   └── static/
│       ├── css/
│       └── js/
├── requirements.txt
├── .env                            # não versionado — ver seção de configuração
└── README.MD
```

---

## Pré-requisitos

- **Python 3.12+**
- **MySQL 8+** (ou compatível) em execução, local ou remoto
- Uma **API Key da AlienVault OTX** ([otx.alienvault.com](https://otx.alienvault.com/) → crie uma conta gratuita → área de configurações do usuário)
- Uma **API Key do Google Gemini** ([Google AI Studio](https://aistudio.google.com/)) — necessária apenas para a funcionalidade de resumo com IA

---

## Instalação e configuração

1. **Clone o repositório**

   ```bash
   git clone <url-do-repositorio>
   cd threat-intelligence
   ```

2. **Crie e ative um ambiente virtual**

   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # Linux / macOS
   source .venv/bin/activate
   ```

3. **Instale as dependências**

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuração do banco de dados

O script **`app/database/DB.sql`** contém tudo que é necessário para criar a base:

1. Conecte-se ao seu servidor MySQL (via terminal, MySQL Workbench, DBeaver etc.).
2. Execute o conteúdo de `app/database/DB.sql`, que:
   - Cria o banco `threat_intelligence`.
   - Cria a tabela `consulta` (armazena cada consulta realizada, com o resultado completo em JSON).
   - Adiciona a coluna `resumo_ia` (resumo gerado por IA).
   - Cria um **evento agendado** (`limpar_consultas_antigas`) que roda 1x por dia e apaga automaticamente consultas com mais de 30 dias.

> Atenção: o script contém, no meio dele, um `TRUNCATE TABLE consulta;` (usado durante o desenvolvimento). Revise o script antes de rodá-lo em um ambiente com dados que você queira preservar.

### Estrutura da tabela `consulta`

| Coluna | Tipo | Descrição |
|---|---|---|
| `id` | INT UNSIGNED, PK, auto-increment | Identificador da consulta |
| `indicador` | VARCHAR(255) | Valor consultado (IP, URL ou hash) |
| `tipo` | ENUM('ip','dominio','hash') | Tipo do indicador |
| `fonte` | VARCHAR(50) | Fonte da consulta (sempre `"OTX"` atualmente) |
| `dataConsulta` | DATETIME | Data/hora da consulta |
| `resultado` | JSON | Resposta completa da OTX já tratada (schema `IndicatorResponse`) |
| `resumo_ia` | TEXT, nullable | Resumo gerado por IA (se solicitado) |

---

## Variáveis de ambiente (.env)

Crie um arquivo `.env` na raiz do projeto (mesmo nível da pasta `app/`) com as variáveis abaixo. **Nunca versione esse arquivo** — ele já está listado no `.gitignore`.

```env
# API da AlienVault OTX
OTX_API_KEY=sua_chave_aqui

# Conexão com o MySQL
DB_HOST=localhost
DB_PORT=3306
DB_NAME=threat_intelligence
DB_USER=seu_usuario
DB_PASSWORD=sua_senha

# API do Google Gemini (resumo com IA)
GEMINI_API_KEY=sua_chave_aqui
```

| Variável | Obrigatória | Descrição |
|---|---|---|
| `OTX_API_KEY` | Sim | Chave de API da AlienVault OTX, usada em toda consulta de indicador |
| `DB_HOST` | Sim | Host do servidor MySQL |
| `DB_PORT` | Sim | Porta do MySQL (padrão `3306`) |
| `DB_NAME` | Sim | Nome do banco (`threat_intelligence`, se seguir o script padrão) |
| `DB_USER` | Sim | Usuário do banco |
| `DB_PASSWORD` | Sim | Senha do usuário do banco |
| `GEMINI_API_KEY` | Somente para o resumo com IA | Chave de API do Google Gemini |

---

## Executando o projeto

Com o ambiente virtual ativado e o `.env` configurado:

```bash
uvicorn app.main:app --reload
```

A aplicação sobe por padrão em `http://127.0.0.1:8000`.

- Página principal (consulta de indicadores): `http://127.0.0.1:8000/indicators`
- Histórico: `http://127.0.0.1:8000/history`

> A raiz (`/`) não possui rota definida — acesse diretamente `/indicators`.

---

## Como usar

1. Acesse `/indicators`.
2. Digite um indicador no campo de busca — pode ser:
   - um **IPv4** (ex.: `8.8.8.8`);
   - uma **URL** completa (ex.: `http://exemplo.com/malware`);
   - um **hash** MD5, SHA1 ou SHA256 de um arquivo.
3. Clique em **Consultar**. O tipo do indicador é detectado automaticamente — não é necessário informá-lo.
4. O dashboard é preenchido com os dados retornados pela OTX (reputação, Pulses, localização, infraestrutura, contexto de ameaça e gráficos).
5. Opcionalmente, clique em **Gerar resumo com IA** para obter um briefing em linguagem simples sobre o indicador consultado.
6. Toda consulta bem-sucedida é salva automaticamente — acesse **Histórico** para revisitá-la depois.
7. No histórico, clique em **Visualizar** para reabrir o dashboard completo daquela consulta (incluindo o resumo de IA, se ele tiver sido gerado no momento da consulta original).

---

## Capturas de tela

### Consulta de indicador

![Campo de pesquisa vazio](capturas%20de%20tela/PesquisaVazia.jpeg)

### Dashboard de resultado

![Dashboard - visão geral](capturas%20de%20tela/DashboardYoutube.jpeg)

![Dashboard - KPIs](capturas%20de%20tela/DashboardYoutube2.jpeg)

![Dashboard - localização e infraestrutura](capturas%20de%20tela/DashboardYoutube3.jpeg)

![Dashboard - contexto de ameaça](capturas%20de%20tela/DashboardYoutube4.jpeg)

![Dashboard - gráficos](capturas%20de%20tela/DashboardYoutube5.jpeg)

![Dashboard - pulses](capturas%20de%20tela/DashboardYoutube6.jpeg)

### Resumo gerado por IA

![Resumo da análise gerado por IA](capturas%20de%20tela/ResumoDeIA.jpeg)

### Histórico de consultas

![Lista de consultas realizadas](capturas%20de%20tela/HistoricoConsultas.jpeg)

### Detalhes de uma consulta do histórico

![Dashboard de uma consulta salva no histórico](capturas%20de%20tela/DashboardHistorico.jpeg)

![Resumo de IA salvo no histórico](capturas%20de%20tela/ResumoDeIAHistorico.jpeg)

---

## Rotas da aplicação

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/indicators` | Página principal (formulário de consulta) |
| `GET` | `/indicators/{indicator}` | Consulta o indicador na OTX, salva no banco e retorna o resultado (JSON) |
| `POST` | `/ai/summary?consulta_id={id}` | Gera o resumo com IA para um resultado já consultado |
| `GET` | `/history` | Página de histórico (últimas consultas, renderizada no servidor) |
| `GET` | `/history/details/{id}` | Página de detalhes de uma consulta (SSR — estrutura da página) |
| `GET` | `/history/details/{id}/data` | Dados completos de uma consulta específica (JSON) |

---

## Fluxos de funcionamento (diagramas)

> Espaço reservado para os diagramas de sequência elaborados durante o desenvolvimento do projeto (consultar indicador, gerar resumo com IA, listar histórico e visualizar detalhes).

### Fluxo 1 — Consultar indicador

![Diagrama de sequência - Consultar indicador](diagramas%20de%20sequência/Fluxo%2001%20-%20Consultar%20indicador.svg)

### Fluxo 2 — Gerar resumo com IA

![Diagrama de sequência - Gerar resumo com IA](diagramas%20de%20sequência/Fluxo%2002%20-%20Gerar%20resumo%20com%20IA.svg)

### Fluxo 3 — Histórico (listagem)

![Diagrama de sequência - Histórico](diagramas%20de%20sequência/Fluxo%2003%20-%20Histórico%20.svg)

### Fluxo 4 — Histórico → Detalhes da consulta

![Diagrama de sequência - Detalhes do histórico](diagramas%20de%20sequência/Fluxo%2004%20-%20Detalhes%20do%20histórico.svg)

---

## Limitações conhecidas / próximos passos

- Não há autenticação de usuários — qualquer pessoa com acesso à aplicação pode consultar e ver o histórico.
- O tratamento de erros da OTX repassa `RuntimeError` como `HTTPException 502` de forma genérica; um versionamento futuro pode especializar os tipos de erro.
- A tela de detalhes do histórico faz duas requisições ao backend (uma para a página, outra para os dados) — ambas acabam consultando o mesmo registro no banco; há espaço para simplificação.
- Não existem testes automatizados no projeto até o momento.
- A geração de resumo com IA depende de uma chave paga/gratuita do Google Gemini e está sujeita aos limites de uso da conta configurada.

---

## Aviso sobre o processo de desenvolvimento

Este projeto foi desenvolvido com apoio de ferramentas de inteligência artificial. A geração inicial de código, estruturação das funcionalidades e documentação contou majoritariamente com o auxílio do **ChatGPT**. A revisão técnica mais aprofundada, identificação e correção de bugs, e refinamento da lógica do projeto foram realizados com apoio do **Claude AI (Anthropic)**.

