import copy
from dataclasses import dataclass

from langchain_core.language_models import BaseChatModel

from log import logger
from presentation.api_v1.providers.gitlab.schemas import CommentOnMergeRequestGitlabEvent
from application.services.graphs import get_code_suggestion_graph
from application.vcs_providers import BaseProvider

from .base import BaseCodeSuggestService


@dataclass
class CodeSuggestService(BaseCodeSuggestService):
    vcs_provider: BaseProvider
    llm: BaseChatModel

    async def suggest_code(self, comment_on_mr_event: CommentOnMergeRequestGitlabEvent) -> None:
        if "/aiva" not in comment_on_mr_event.object_attributes.note:
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
        code_suggestion_graph = get_code_suggestion_graph(llm=self.llm)

        code_suggestion = await code_suggestion_graph.ainvoke({
            "code_snippet": code_snippet,
            "user_comment": user_comment,
            "result": ""})
        code_suggestion: str = code_suggestion["result"].content
        logger.info("LLM response", response=code_suggestion)

        new_line_char = '\n'
        answer = "```suggestion:-{original_code_len}+{code_suggestion_len}\n{code_suggestion}\n```"

        original_code_len = len(code_snippet.split(new_line_char))
        code_suggestion_len = len(code_suggestion.split(new_line_char))

        answer = answer.format(
            original_code_len=original_code_len, 
            code_suggestion_len=code_suggestion_len, 
            code_suggestion=code_suggestion)
        logger.info("Code suggestion", answer=answer, original_code_len=original_code_len, code_suggestion_len=code_suggestion_len)

        return answer
