from fastapi import FastAPI
from app.api.indicators import router as indicators_router      # para deixar claro no main.py que aquele router pertence aos indicadores.
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")    # "FastAPI, quando alguém acessar determinado caminho, procure os arquivos em determinada pasta."

app.include_router(indicators_router)                           # "FastAPI, inclua nesse aplicativo todas as rotas que estão dentro desse router."