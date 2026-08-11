from typing import List

from pydantic import BaseModel


class CategoryCreate(BaseModel):
    """
    Schema for request to create a category
    """

    name: str
    description: str
    examples: list[str]


class CategoryRead(BaseModel):
    """
    Schema for returning a category
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
    category_id: int
    category_name: str


class CategorizedTweetsOutput(BaseModel):
    """
    A list of categorized_tweets
    """

    categorized_tweets: List[CategorizedTweetOutput]
