from fastapi import FastAPI, Response, status
from presentation.api_v1 import api_v1

app = FastAPI(title="Aiva")

app.include_router(api_v1)


@app.get("/")
async def liveness_probe() -> Response:
    return Response(status_code=status.HTTP_200_OK, content="Aiva API is running!")
