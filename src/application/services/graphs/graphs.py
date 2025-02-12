#TODO i don't like how it looks. I belive it is better to put this inside NodeProvider class as parameter
from .prompts import gigachat_prompts
from log import logger

from dataclasses import dataclass
from langchain_core.language_models import BaseChatModel
from pydantic import BaseModel
from langgraph.graph import END, StateGraph, START
import copy

#TODO seems like langgraphs nodes can work with only one state at a time. For now here lyes big, fat state with everything we need to generate code suggestion. But i would like to make it more "general-porpuse" in the future
class CodeSuggestionState(BaseModel):
    code_snippet: str
    user_comment: str
    result: str
    #validation_comment: str
    #iteration: int

@dataclass
class CodeSuggestionNodeProvider():
    llm: BaseChatModel

    async def generate_result(self, state: CodeSuggestionState) -> CodeSuggestionState:
        prompt = copy.deepcopy(gigachat_prompts.generate_code_request)
        prompt.user = prompt.user.format(
            user_comment=state.user_comment, 
            code_snippet=state.code_snippet)

        result = await self.llm.ainvoke(prompt.messages)
        
        return {'result': result}
    
    async def validate_result(self, state: CodeSuggestionState) -> CodeSuggestionState:
        # with structured output
        #result = await self.llm.with_structured_output(s1).ainvoke(prompt.messages)
        pass
    
    async def update_result(self, state: CodeSuggestionState) -> CodeSuggestionState:
        pass


def get_code_suggestion_graph(llm: BaseChatModel) -> StateGraph:
    np = CodeSuggestionNodeProvider(llm)
    #TODO decided to left reflection steps for now. Will be back later to finish it. Inspirated by this https://github.com/langchain-ai/langgraph/blob/main/docs/docs/tutorials/code_assistant/langgraph_code_assistant.ipynb
    workflow = StateGraph(CodeSuggestionState)

    # Define the nodes
    workflow.add_node("generate", np.generate_result)  # generation solution
    
    # Build graph
    workflow.add_edge(START, "generate")
    workflow.add_edge("generate", END)
    logger.info("Created LLM graph")
    
    return workflow.compile() 
