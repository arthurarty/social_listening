from langchain.chat_models import init_chat_model

from app.config import settings

claude_sonnet = init_chat_model(
    settings.claude_sonnet_model,
    api_key=settings.anthropic_api_key,
    timeout=600,
    max_tokens=4000,
    streaming=True,
    output_config={"effort": "low"},
)
