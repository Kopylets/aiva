import copy
from dataclasses import dataclass

from langchain_core.language_models import BaseChatModel

from log import logger
from presentation.api_v1.providers.gitlab.schemas import CommentOnMergeRequestGitlabEvent
from prompts import gigachat_prompts
from application.vcs_providers import BaseProvider

from .base import BaseCodeSuggestService


@dataclass
class CodeSuggestService(BaseCodeSuggestService):
    vcs_provider: BaseProvider
    llm: BaseChatModel

    async def suggest_code(self, comment_on_mr_event: CommentOnMergeRequestGitlabEvent) -> None:
        if "@aiva" not in comment_on_mr_event.object_attributes.note:
            return
        code_snippet = await self.vcs_provider.get_code_snippet_from_path(
            project_path=comment_on_mr_event.project.path_with_namespace,
            file_path=comment_on_mr_event.object_attributes.position.new_path,
            mr_id=comment_on_mr_event.merge_request.merge_request_iid,
            start_line=comment_on_mr_event.object_attributes.position.line_range.start.new_line,
            end_line=comment_on_mr_event.object_attributes.position.line_range.end.new_line,
        )
        code_suggestion = await self._suggest_code(
            user_comment=comment_on_mr_event.object_attributes.note,
            code_snippet=code_snippet
        )
        await self.vcs_provider.publish_code_suggestion(
            code_suggestion,
            comment_on_mr_event.project.path_with_namespace,
            comment_on_mr_event.object_attributes.discussion_id,
            comment_on_mr_event.merge_request.merge_request_iid
        )

    async def _suggest_code(self, user_comment: str, code_snippet: str) -> str:
        # Gleb, your code is here! Here is an example of how to call model

        # Copy prompt template
        copy_prompt = copy.deepcopy(gigachat_prompts.comment_code_suggest_prompt)

        # Change with your values
        copy_prompt.user = copy_prompt.user.format(user_comment=user_comment, code=code_snippet)

        # Invoke model, or maybe use `with_structured_output` or smth...
        code_suggestion = await self.llm.ainvoke(copy_prompt.messages)
        logger.info("LLM response", response=code_suggestion)

        return code_suggestion.content
