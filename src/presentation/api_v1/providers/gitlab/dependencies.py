from json import JSONDecodeError
from typing import TypeAlias, Annotated

from fastapi import Request, HTTPException, status, Depends
from pydantic import ValidationError

from .schemas.base import BaseGitlabEvent
from .schemas.comment import CommentGitlabEvent, CommentOnCodeSnippetEvent

JSON: TypeAlias = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None


async def decode_request(request: Request) -> JSON:
    try:
        json_response = await request.json()
    except JSONDecodeError as json_decode_error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=json_decode_error.msg)
    return json_response


async def validate_gitlab_event(json_request: Annotated[JSON, Depends(decode_request)]) -> BaseGitlabEvent:
    try:
        gitlab_event = BaseGitlabEvent.model_validate(json_request)
    except ValidationError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Event is not a valid gitlab event: {ve}")
    return gitlab_event


async def parse_gitlab_request(
    gitlab_event: Annotated[BaseGitlabEvent, Depends(validate_gitlab_event)],
    json_request: Annotated[JSON, Depends(decode_request)],
) -> BaseGitlabEvent:
    # Comment event
    if gitlab_event.event_type == "note":
        comment_event = CommentGitlabEvent.model_validate(json_request)

        # Comment on code snippet
        if comment_event.object_attributes.noteable_type == "Snippet":
            return CommentOnCodeSnippetEvent.model_validate(json_request)

        # Comment on merge request
        elif comment_event.object_attributes.noteable_type == "MergeRequest":
            pass

    # MergeRequest event
    elif gitlab_event.event_type == "merge_request":
        pass

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Event is not supported")
