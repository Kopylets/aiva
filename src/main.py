import logfire
from fastapi import FastAPI, Response, Request, status
from presentation.api_v1 import api_v1

from log import logger

app = FastAPI(title="Aiva", logger=logger)

app.include_router(api_v1)

logfire.instrument_fastapi(app, excluded_urls=r"^https?://[^/]+/$")


@app.get("/")
async def liveness_probe() -> Response:
    return Response(status_code=status.HTTP_200_OK, content="Aiva API is running!")
