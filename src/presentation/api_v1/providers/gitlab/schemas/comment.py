"""Comment Gitlab WebHooks Schemas"""

from typing import Literal

from pydantic import BaseModel, Field

from .base import GitlabDateTime, BaseGitlabEvent


# ====================================================
#               Base comment schemas
# ====================================================
class CommentStDiff(BaseModel):
    diff: str
    new_path: str
    old_path: str
    a_mode: str
    b_mode: str
    new_file: bool
    renamed_file: bool
    deleted_file: bool


class CommentObjectAttributes(BaseModel):
    object_attributes_id: int = Field(alias="id")
    note: str
    noteable_type: Literal["Commit", "MergeRequest", "Issue", "Snippet"]
    author_id: int
    created_at: GitlabDateTime
    updated_at: GitlabDateTime
    project_id: int
    attachment: None
    line_code: str | None
    commit_id: str
    noteable_id: int
    system: bool
    st_diff: CommentStDiff | None
    action: Literal["create", "update"]
    url: str


class CommentGitlabEvent(BaseGitlabEvent):
    object_attributes: CommentObjectAttributes


# ====================================================
#         Comment on a code snippet schemas
# ====================================================
class CommentSnippet(BaseModel):
    id: int
    title: str
    description: str
    content: str
    author_id: int
    project_id: int
    created_at: GitlabDateTime
    updated_at: GitlabDateTime
    file_name: str
    type: Literal["ProjectSnippet"]
    visibility_level: int
    url: str


class CommentOnCodeSnippetEvent(CommentGitlabEvent):
    snippet: CommentSnippet


# ====================================================
#         Comment on an issue schemas
# ====================================================
class CommentOnIssueEvent(CommentGitlabEvent):
    pass
