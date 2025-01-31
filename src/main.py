from fastapi import FastAPI
from presentation.api_v1 import api_v1

app = FastAPI(title="Aiva")

app.include_router(api_v1)
