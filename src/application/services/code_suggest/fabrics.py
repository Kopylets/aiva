from typing import Annotated

from fastapi import Depends

from application.vcs_providers import (
    BaseProvider,
    get_bitbucket_vcs_provider,
    get_gitlab_vcs_provider,
)

from .base import BaseCodeSuggestService
from .code_suggest_service import CodeSuggestService


def get_code_suggest_service_gitlab_provider(
    gitlab_provider: Annotated[BaseProvider, Depends(get_gitlab_vcs_provider)],
) -> BaseCodeSuggestService:
    return CodeSuggestService(vcs_provider=gitlab_provider)


def get_code_suggest_service_bitbucket_provider(
    bitbucket_provider: Annotated[BaseProvider, Depends(get_bitbucket_vcs_provider)],
) -> BaseCodeSuggestService:
    return CodeSuggestService(vcs_provider=bitbucket_provider)
