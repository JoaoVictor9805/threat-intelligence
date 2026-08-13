from fastapi import FastAPI
from app.api.indicators import router as indicators_router      # para deixar claro no main.py que aquele router pertence aos indicadores.

app = FastAPI()

app.include_router(indicators_router)                           # "FastAPI, inclua nesse aplicativo todas as rotas que estão dentro desse router."