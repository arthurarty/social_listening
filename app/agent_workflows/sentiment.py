"""
Categorize a tweet.
"""

from typing import Any, Dict, List

from app.agents.sentiment_agent import SENTIMENT_DICT, sentiment_agent
from app.logger import logger
from app.schemas.twitter_schema import TweetMinimal, TweetSentimentList
from app.services.instances import twitter_service


def analyze_tweets(
    tweets: List[TweetMinimal], sentiment_data: Dict[str, Any]
) -> TweetSentimentList:
    """
    Using an LLM figure the sentiment of a tweet.
    """
    logger.info("Analyzing %s tweets.", len(tweets))
    result = sentiment_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"Sentiment Data: {sentiment_data}\n\nTweets: {tweets}",
                }
            ]
        }
    )
    output = result["structured_response"]
    return output


def main(no_of_tweets: int = 3, skip: int = 0) -> int:
    """
    Read tweets from the database and run sentiment analysis.

    Returns no of tweets read from the database
    """
    tweets = twitter_service.get_tweets_minimal(
        tweet_lang="en", limit=no_of_tweets, skip=skip, has_sentiment=False
    )
    if len(tweets) == 0:
        logger.warning("No tweets to process")
        return 0
    analyzed_tweets = analyze_tweets(tweets, sentiment_data=SENTIMENT_DICT)
    logger.info("Analyzed_Tweets: %s", len(analyzed_tweets.tweets))
    twitter_service.bulk_update_tweet_sentiment(analyzed_tweets)
    logger.info("Done!")
    return len(tweets)
