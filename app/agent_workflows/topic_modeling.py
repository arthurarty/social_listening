"""
An agent that reads text and assigns a topic to it.
"""

from contextlib import contextmanager
from typing import Any, Dict, List

from app.agents.topic_agent import topic_agent
from app.database.connection import get_session
from app.logger import logger
from app.schemas.topic_schema import CategorizedTweetsOutput, TopicRead
from app.schemas.twitter_schema import TweetMinimal
from app.services.instances import topic_service, twitter_service


def assign_topics(
    tweets: List[TweetMinimal], topics_data: List[Dict[str, Any]]
) -> CategorizedTweetsOutput:
    """
    For each tweet in the list of tweets, this functions assigns a topic.
    The topic assigned comes from the topics in the topics_data.
    """
    result = topic_agent.invoke(
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
