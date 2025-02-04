"""Base Gitlab WebHooks schemas"""

from datetime import datetime
from typing import Annotated, Literal

from pydantic import PlainValidator, AwareDatetime, BaseModel, Field

GitlabDateTime = Annotated[
    AwareDatetime,
    PlainValidator(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S %Z")),
]


class GitlabUser(BaseModel):
    user_id: int = Field(alias="id")
    name: str
    username: str
    avatar_url: str
    email: str


class GitlabProject(BaseModel):
    project_id: int = Field(alias="id")
    name: str
    description: str | None
    web_url: str
    avatar_url: str | None
    git_ssh_url: str
    git_http_url: str
    namespace: str
    visibility_level: int
    path_with_namespace: str
    default_branch: str
    ci_config_path: str | None
    homepage: str
    url: str
    ssh_url: str
    http_url: str


class GitlabRepository(BaseModel):
    name: str
    url: str
    description: str | None
    homepage: str


class BaseGitlabEvent(BaseModel):
    object_kind: Literal["note", "merge_request"]
    event_type: Literal["note", "merge_request"]
    user: GitlabUser
    project_id: int
    project: GitlabProject
    repository: GitlabRepository
