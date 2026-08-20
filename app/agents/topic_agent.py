"""
An agent that reads text and assigns a topic to it.
"""

from contextlib import contextmanager
from typing import Any, Dict, List

from langchain.agents import create_agent

from app.database.connection import get_session
from app.logger import logger
from app.schemas.topic_schema import CategorizedTweetsOutput, TopicRead
from app.schemas.twitter_schema import TweetMinimal
from app.services.instances import topic_service, twitter_service

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


# ollama_gemma4 = init_chat_model(
#     "ollama:gemma4",
#     temperature=0,
#     timeout=300,
# )

agent = create_agent(
    model="ollama:gemma4",
    system_prompt=SYSTEM_PROMPT,
    response_format=CategorizedTweetsOutput,
)


def assign_topics(
    tweets: List[TweetMinimal], topics_data: List[Dict[str, Any]]
) -> CategorizedTweetsOutput:
    """
    For each tweet in the list of tweets, this functions assigns a topic.
    The topic assigned comes from the topics in the topics_data.
    """
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"Topics: {topics_data}\n\nTweets: {tweets}",
                }
            ]
        }
    )
    output = result["structured_response"]
    return output


def main(no_of_tweets: int = 3, skip: int = 0) -> int:
    """
    Read tweets from the database and assign them into topics.
    The topics exist in the topics table.

    Returns no of tweets read from the database
    """
    with contextmanager(get_session)() as session:
        logger.info("Pulling Topics")
        topics = topic_service.get_topics(session)
        topics_data = [TopicRead.model_validate(topic).model_dump() for topic in topics]
    logger.info("Pulling tweets")
    tweets = twitter_service.get_tweets_minimal(
        tweet_lang="en", limit=no_of_tweets, skip=skip, is_categorized=False
    )
    if len(tweets) == 0:
        return 0
    logger.info("Assigning topics")
    categorized_tweets = assign_topics(tweets, topics_data)
    logger.info("Categorized_Tweets: %s", len(categorized_tweets.categorized_tweets))
    logger.info("Persisting changes to db.")
    twitter_service.bulk_update_tweet_topic(categorized_tweets)
    return len(tweets)
