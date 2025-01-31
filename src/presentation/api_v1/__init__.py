from fastapi import APIRouter

from .providers import gitlab_router

api_v1 = APIRouter(prefix="/api/v1")

api_v1.include_router(gitlab_router)

__all__ = ["api_v1"]
