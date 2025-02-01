from fastapi import FastAPI, Response, Request, status
from presentation.api_v1 import api_v1

from log import logger

app = FastAPI(title="Aiva", logger=logger)

app.include_router(api_v1)


@app.middleware("http")
async def add_logs(request: Request, call_next):
    response = await call_next(request)
    if request.url.path == "/":
        return response
    logger.info(
        f'{request.client.host}:{request.client.port} - '
        f'"{request.method} {request.url.path} HTTP/1.1" {response.status_code}'
    )
    return response


@app.get("/")
async def liveness_probe() -> Response:
    return Response(status_code=status.HTTP_200_OK, content="Aiva API is running!")
