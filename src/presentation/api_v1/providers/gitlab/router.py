from typing import Annotated

from fastapi import APIRouter, Response, BackgroundTasks, status, Depends

from application.services.comment_code_suggest import (
    BaseCodeSuggestService,
    get_code_suggest_service_gitlab_provider,
)
from .dependencies import parse_gitlab_request
from .schemas import BaseGitlabEvent
from .schemas import CommentOnMergeRequestEvent

gitlab_router = APIRouter(prefix="/gitlab", tags=["Gitlab"])


@gitlab_router.post("/webhook", description="Accepts a webhooks from gitlab")
async def gitlab_webhook(
    background_tasks: BackgroundTasks,
    gitlab_event: Annotated[BaseGitlabEvent, Depends(parse_gitlab_request)],
    code_suggest_service: Annotated[BaseCodeSuggestService, Depends(get_code_suggest_service_gitlab_provider)],
) -> Response:
    if isinstance(gitlab_event, CommentOnMergeRequestEvent):
        background_tasks.add_task(code_suggest_service.suggest_code, comment_on_mr_code_snippet=gitlab_event)
    return Response(status_code=status.HTTP_200_OK, content="OK")
