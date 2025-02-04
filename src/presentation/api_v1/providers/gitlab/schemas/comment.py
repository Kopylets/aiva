"""Comment Gitlab WebHooks Schemas"""

from datetime import datetime
from typing import Literal, Any

from pydantic import BaseModel, Field

from .base import GitlabDateTime, BaseGitlabEvent, GitlabProject


# ========================================================================================================
#                                  Base comment events schemas.
#
#   https://docs.gitlab.com/ee/user/project/integrations/webhook_events.html#comment-events
# ========================================================================================================
class StDiff(BaseModel):
    diff: str
    new_path: str
    old_path: str
    a_mode: str
    b_mode: str
    new_file: bool
    renamed_file: bool
    deleted_file: bool


class BaseLineRange(BaseModel):
    line_code: str
    # TODO: fix - add more types?
    type: Literal["new"]
    old_line: int | None
    new_line: int | None


class LineRange(BaseModel):
    start: BaseLineRange
    end: BaseLineRange


class Position(BaseModel):
    base_sha: str | None
    start_sha: str | None
    head_sha: str | None
    old_path: str | None
    new_path: str | None
    # TODO: fix - add more types?
    position_type: Literal["text"]
    old_line: int | None
    new_line: int | None
    line_range: LineRange | None


class CommentObjectAttributes(BaseModel):
    # TODO: fix Any type
    attachment: Any
    author_id: int
    change_position: Position
    commit_id: str | None
    created_at: GitlabDateTime | datetime
    discussion_id: str
    note: str
    noteable_id: int
    noteable_type: Literal["Commit", "MergeRequest", "Issue", "Snippet"]
    original_position: Position
    position: Position
    project_id: int
    resolved_at: GitlabDateTime | datetime | None
    resolved_by_id: int | None
    # TODO: fix Any type
    resolved_by_push: Any
    st_diff: StDiff | None
    system: bool
    # TODO: fix - add more types?
    type: Literal["DiffNote"]
    updated_at: GitlabDateTime | datetime
    updated_by_id: int | None
    description: str
    url: str
    action: Literal["create", "update"]


class CommentGitlabEvent(BaseGitlabEvent):
    object_attributes: CommentObjectAttributes


# ========================================================================================================
#                               Comment on a merge request schemas
#
#   https://docs.gitlab.com/ee/user/project/integrations/webhook_events.html#comment-on-a-merge-request
# ========================================================================================================
class CommitAuthor(BaseModel):
    name: str
    email: str


class LastCommit(BaseModel):
    last_commit_id: str = Field(alias="id")
    message: str
    title: str
    timestamp: GitlabDateTime | datetime
    url: str
    author: CommitAuthor


class MergeParams(BaseModel):
    force_remove_source_branch: str


class MergeRequest(BaseModel):
    assignee_id: int | None
    author_id: int
    created_at: GitlabDateTime | datetime
    description: str
    draft: bool
    head_pipeline_id: int
    merge_request_id: int = Field(alias="id")
    merge_request_iid: int = Field(alias="iid")
    last_edited_at: GitlabDateTime | datetime | None
    last_edited_by_id: int | None
    merge_commit_sha: str | None
    merge_error: str | None
    merge_params: MergeParams
    merge_status: str
    merge_user_id: int | None
    merge_when_pipeline_succeeds: bool
    milestone_id: int | None
    source_branch: str
    source_project_id: int
    state_id: int
    target_branch: str
    target_project_id: int
    time_estimate: int
    title: str
    updated_at: GitlabDateTime | datetime
    updated_by_id: int | None
    prepared_at: GitlabDateTime | datetime
    assignee_ids: list[int]
    blocking_discussions_resolved: bool
    detailed_merge_status: str
    first_contribution: bool
    human_time_change: str | None
    human_time_estimate: str | None
    human_total_time_spent: str | None
    labels: list[str]
    last_commit: LastCommit
    reviewer_ids: list[int]
    source: GitlabProject
    state: str
    target: GitlabProject
    time_change: int
    total_time_spent: int
    url: str
    work_in_progress: bool
    # TODO: fix Any type
    approval_rules: list[Any] = Field(default_factory=list)


class CommentOnMergeRequestGitlabEvent(CommentGitlabEvent):
    merge_request: MergeRequest
