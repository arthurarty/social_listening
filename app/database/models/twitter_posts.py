from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


class TwitterPost(SQLModel, table=True):
    """
    Represents a single twitter/post
    """

    id: int | None = Field(default=None, primary_key=True)
    tweet_id: str = Field(unique=True)
    type: str
    url: str
    twitter_url: str
    text: str
    source: str
    retweet_count: int = Field(default=0)
    reply_count: int = Field(default=0)
    like_count: int = Field(default=0)
    quote_count: int = Field(default=0)
    view_count: int = Field(default=0)
    created_at: datetime
    lang: str | None = Field(default=None)
    bookmark_count: int = Field(default=0)
    is_reply: bool = Field(default=False)
    in_reply_to_id: str | None = Field(default=None)
    conversation_id: str | None = Field(default=None)
    in_reply_to_user_id: str | None = Field(default=None)
    in_reply_to_username: str | None = Field(default=None)
    author: dict = Field(sa_column=Column(JSONB))
    card: dict | None = Field(default=None, sa_column=Column(JSONB))
    place: dict | None = Field(default=None, sa_column=Column(JSONB))
    hashtags: str | None = Field(default=None)
    user_mentions: str | None = Field(default=None)
    quoted_tweet: dict | None = Field(default=None, sa_column=Column(JSONB))
    retweeted_tweet: dict | None = Field(default=None, sa_column=Column(JSONB))
    is_limited_reply: bool = Field(default=False)
    community_info: dict | None = Field(default=None, sa_column=Column(JSONB))
    article: dict | None = Field(default=None, sa_column=Column(JSONB))
