from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from app.config import settings


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


model = init_chat_model(
    "claude-sonnet-4-6",
    api_key=settings.anthropic_api_key,
    temperature=0.5,
    timeout=600,
    max_tokens=1000,
    streaming=True,
)

agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
print(result["messages"][-1].content_blocks)
