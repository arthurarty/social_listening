from typing import List

from pydantic import BaseModel


class TopicCreate(BaseModel):
    """
    Schema for request to create a topic
    """

    name: str
    description: str
    examples: list[str]


class TopicRead(BaseModel):
    """
    Schema for returning a topic
    """

    id: int
    name: str
    description: str
    examples: list[str]

    class Config:
        from_attributes = True


class CategorizedTweetOutput(BaseModel):
    """
    Schema for categorizing a tweet.
    """

    tweet_id: int
    tweet_text: str
    topic_id: int
    topic_name: str


class CategorizedTweetsOutput(BaseModel):
    """
    A list of categorized_tweets
    """

    categorized_tweets: List[CategorizedTweetOutput]
