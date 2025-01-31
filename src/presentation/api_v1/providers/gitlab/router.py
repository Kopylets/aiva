from pprint import pprint
from typing import Annotated, Any

from fastapi import APIRouter, Response, BackgroundTasks, status, Depends

from application.services.code_suggest import (
    BaseCodeSuggestService,
    get_code_suggest_service_gitlab_provider,
)
from .dependencies import parse_gitlab_request

gitlab_router = APIRouter(prefix="/gitlab", tags=["Gitlab"])


@gitlab_router.post("/webhook", description="Accepts a webhooks from gitlab")
async def gitlab_webhook(
    background_tasks: BackgroundTasks,
    request: Annotated[Any, Depends(parse_gitlab_request)],
    code_suggest_service: Annotated[
        BaseCodeSuggestService, Depends(get_code_suggest_service_gitlab_provider)
    ],
) -> Response:
    pprint(request)
    background_tasks.add_task(code_suggest_service.suggest_code, comment=str(request))
    return Response(status_code=status.HTTP_200_OK)
