from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List

from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlmodel import select

from app.database.connection import db_session
from app.database.models.tweets import Tweet
from app.schemas.topic_schema import CategorizedTweetsOutput
from app.schemas.twitter_schema import TweetMinimal, TweetResult, TweetSearchResult

TWITTER_CREATED_AT_FORMAT = "%a %b %d %H:%M:%S %z %Y"


class TwitterServiceInterface(ABC):
    """
    The Twitter service will implement this interface.
    """

    @abstractmethod
    def convert_json_to_pydantic_model(
        self, input_dict: Dict[str, Any]
    ) -> TweetSearchResult:
        """
        Convert dict from API to Pydantic model
        """

    @abstractmethod
    def convert_tweet_search_results_to_db_model(
        self, tweet_search_results: TweetSearchResult
    ) -> List[Tweet]:
        """
        Converts the search results to a list Tweet(db model)
        """

    @abstractmethod
    def store_tweets(self, tweets: List[Tweet]) -> str:
        """
        Persists the tweets to the database
        """

    @abstractmethod
    def get_tweets_as_text(
        self, tweet_lang: str | None = None, limit: int = 100, skip: int = 0
    ) -> List[str]:
        """
        Return only the text of the tweets, optionally filtered by language
        """

    @abstractmethod
    def bulk_update_tweet_topic(
        self, categorized_tweets_output: CategorizedTweetsOutput
    ) -> None:
        """
        A bulk update topics for given tweets
        """


class TwitterServiceImpl(TwitterServiceInterface):
    def convert_json_to_pydantic_model(
        self, input_dict: Dict[str, Any]
    ) -> TweetSearchResult:
        """
        Convert dict from API to Pydantic model
        """
        return TweetSearchResult.model_validate(input_dict)

    def _convert_tweet_result_to_db_model(self, tweet_result: TweetResult) -> Tweet:
        """
        Converts a single TweetResult(pydantic model) to a Tweet(db model)
        """
        hashtags = ",".join(hashtag.text for hashtag in tweet_result.entities.hashtags)
        user_mentions = ",".join(
            mention.screen_name for mention in tweet_result.entities.user_mentions
        )
        return Tweet(
            tweet_id=tweet_result.id,
            type=tweet_result.type,
            url=tweet_result.url,
            twitter_url=tweet_result.twitter_url,
            text=tweet_result.text,
            source=tweet_result.source,
            retweet_count=tweet_result.retweet_count,
            reply_count=tweet_result.reply_count,
            like_count=tweet_result.like_count,
            quote_count=tweet_result.quote_count,
            view_count=tweet_result.view_count,
            created_at=datetime.strptime(
                tweet_result.created_at, TWITTER_CREATED_AT_FORMAT
            ),
            lang=tweet_result.lang,
            bookmark_count=tweet_result.bookmark_count,
            is_reply=tweet_result.is_reply,
            in_reply_to_id=tweet_result.in_reply_to_id,
            conversation_id=tweet_result.conversation_id,
            in_reply_to_user_id=tweet_result.in_reply_to_user_id,
            in_reply_to_username=tweet_result.in_reply_to_username,
            author=(
                tweet_result.author.model_dump(by_alias=True)
                if tweet_result.author
                else {}
            ),
            card=(
                tweet_result.card.model_dump(by_alias=True)
                if tweet_result.card
                else None
            ),
            place=(
                tweet_result.place.model_dump(by_alias=True)
                if tweet_result.place
                else None
            ),
            hashtags=hashtags or None,
            user_mentions=user_mentions or None,
            quoted_tweet=(
                tweet_result.quoted_tweet.model_dump(by_alias=True)
                if tweet_result.quoted_tweet
                else None
            ),
            retweeted_tweet=(
                tweet_result.retweeted_tweet.model_dump(by_alias=True)
                if tweet_result.retweeted_tweet
                else None
            ),
            is_limited_reply=tweet_result.is_limited_reply,
            community_info=tweet_result.community_info,
            article=tweet_result.article,
        )

    def convert_tweet_search_results_to_db_model(
        self, tweet_search_results: TweetSearchResult
    ) -> List[Tweet]:
        """
        Converts the search results to a list Tweet(db model)
        """
        return [
            self._convert_tweet_result_to_db_model(tweet_result)
            for tweet_result in tweet_search_results.tweets
        ]

    def store_tweets(self, tweets: List[Tweet]) -> str:
        """
        Persists the tweets to the database in a single bulk insert.
        Tweets whose tweet_id already exists are skipped.
        """
        if not tweets:
            return "Done"

        values = [tweet.model_dump(exclude={"id"}) for tweet in tweets]
        stmt = (
            pg_insert(Tweet)
            .values(values)
            .on_conflict_do_nothing(index_elements=["tweet_id"])
        )
        with db_session() as session:
            session.execute(stmt)
        return "Done"

    def get_tweets_as_text(
        self, tweet_lang: str | None = None, limit: int = 100, skip: int = 0
    ) -> List[str]:
        """
        Return only the text of the tweets, optionally filtered by language
        """
        statement = select(Tweet.text).order_by(Tweet.id).offset(skip).limit(limit)
        if tweet_lang is not None:
            statement = statement.where(Tweet.lang == tweet_lang)

        with db_session() as session:
            return list(session.execute(statement).scalars().all())

    def get_tweets(
        self, tweet_lang: str | None = None, limit: int = 25, skip: int = 0
    ) -> List[Tweet]:
        """
        Read tweets from the database.
        """
        statement = select(Tweet).order_by(Tweet.id).offset(skip).limit(limit)
        if tweet_lang is not None:
            statement = statement.where(Tweet.lang == tweet_lang)
        with db_session() as session:
            return list(session.execute(statement).scalars().all())

    def get_tweets_minimal(
        self, tweet_lang: str | None = None, limit: int = 25, skip: int = 0
    ) -> List[TweetMinimal]:
        """
        Reads tweets from the database and only returns id and the tweet text.
        """
        statement = (
            select(Tweet.id, Tweet.text).order_by(Tweet.id).offset(skip).limit(limit)
        )
        if tweet_lang is not None:
            statement = statement.where(Tweet.lang == tweet_lang)
        with db_session() as session:
            rows = session.execute(statement).all()
            return [TweetMinimal(id=row.id, text=row.text) for row in rows]

    def bulk_update_tweet_topic(
        self, categorized_tweets_output: CategorizedTweetsOutput
    ) -> None:
        """
        A bulk update topics for given tweets
        """
        tweet_dicts = [
            {"id": tweet.tweet_id, "topic_id": tweet.topic_id}
            for tweet in categorized_tweets_output.categorized_tweets
        ]
        with db_session() as session:
            session.execute(update(Tweet), tweet_dicts)
