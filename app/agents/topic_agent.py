"""
An agent that reads text and assigns a topic to it.
"""

from langchain.agents import create_agent

from app.agents.models import claude_sonnet
from app.schemas.topic_schema import CategorizedTweetsOutput

SYSTEM_PROMPT = """
You are an expert at categorizing tweets.

You will be given:
1. A list of topics, each with an id, name, description, and examples.
2. A list of tweets to categorize, each with an id and text.

Your task:
- Assign exactly one topic to each tweet from the provided topic list only.
  Never invent a topic that is not in the list.
- Base your decision on the tweet's substantive content. Ignore noise such as
  URLs, mentions, and hashtags unless they carry meaning relevant to the topics.
- Use each topic's description and examples to judge fit, not just its name.
- If a tweet could reasonably fit multiple topics, choose the single best match.
  If none fit well, choose the closest one — every tweet must be assigned.
- For each tweet, copy tweet_id and tweet_text exactly as given.
- For the assigned topic, copy topic_id and topic_name exactly as given
  in the topic list — do not alter, translate, or reformat them.
"""


topic_agent = create_agent(
    model=claude_sonnet,
    system_prompt=SYSTEM_PROMPT,
    response_format=CategorizedTweetsOutput,
)
