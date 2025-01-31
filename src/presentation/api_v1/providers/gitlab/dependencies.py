from json import JSONDecodeError
from typing import Any

from fastapi import Request, HTTPException, status


async def parse_gitlab_request(request: Request) -> Any:
    try:
        json_response = await request.json()
    except JSONDecodeError as json_decode_error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=json_decode_error.msg
        )
    return json_response
