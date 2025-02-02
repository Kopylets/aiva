import copy
from dataclasses import dataclass

from langchain_core.language_models import BaseChatModel

from log import logger
from prompts import gigachat_prompts
from application.vcs_providers import BaseProvider
from presentation.api_v1.providers.gitlab.schemas import CommentOnCodeSnippetEvent

from .base import BaseCodeSuggestService


@dataclass
class CodeSuggestService(BaseCodeSuggestService):
    vcs_provider: BaseProvider
    llm: BaseChatModel

    async def suggest_code(self, comment_on_code_snippet: CommentOnCodeSnippetEvent) -> None:
        logger.info("Suggesting code..", comment_on_code_snippet=comment_on_code_snippet)
        code_suggestion = await self._suggest_code(comment_on_code_snippet)
        logger.info("Suggestion", code_suggestion=code_suggestion)

    async def _suggest_code(self, comment_on_code_snippet: CommentOnCodeSnippetEvent) -> str:
        # Gleb, your code is here! Here is an example of how to call model

        # Copy prompt template
        copy_prompt = copy.deepcopy(gigachat_prompts.comment_code_suggest_prompt)

        # Change with your values
        copy_prompt.user = copy_prompt.user.format(what_to_say=comment_on_code_snippet.snippet.content)

        # Invoke model, or maybe use `with_structured_output` or smth...
        code_suggestion = await self.llm.ainvoke(copy_prompt.messages)
        return code_suggestion.content
