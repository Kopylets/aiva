from langchain_gigachat.chat_models import GigaChat
from settings import settings


def get_gigachat_llm() -> GigaChat:
    return GigaChat(
        credentials=settings.llm_settings.api_key.get_secret_value(),
        scope="GIGACHAT_API_CORP",
        temperature=settings.llm_settings.temperature,
        verify_ssl_certs=False,
    )
