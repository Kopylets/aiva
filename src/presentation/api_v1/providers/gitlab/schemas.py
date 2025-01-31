from pydantic import BaseModel


# ====================================================
#               WebHooks from Gitlab
# ====================================================


class CommentCodeSnippetEvent(BaseModel):
    pass


class MergeRequestEvent(BaseModel):
    pass
