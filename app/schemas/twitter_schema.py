from __future__ import annotations

from enum import StrEnum, auto
from typing import Any, List

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SentimentEnum(StrEnum):
    """
    Options for setting sentiment
    """

    POSITIVE = auto()
    NEGATIVE = auto()
    NEUTRAL = auto()
    MIXED = auto()


class UrlEntityDetail(BaseModel):
    """A single URL found within a tweet's text or a user's profile fields"""

    display_url: str
    expanded_url: str
    url: str
    indices: list[int] = []


class HashtagEntity(BaseModel):
    """A hashtag found within a tweet's text or a user's profile fields"""

    text: str
    indices: list[int] = []


class UserMentionEntity(BaseModel):
    """A user mentioned within a tweet's text or a user's profile fields"""

    id_str: str = Field(alias="id_str")
    name: str
    screen_name: str
    indices: list[int] = []

    model_config = ConfigDict(populate_by_name=True)


class ProfileFieldEntities(BaseModel):
    """Entities (urls, hashtags, mentions) extracted from a single profile field"""

    urls: list[UrlEntityDetail] = []
    hashtags: list[HashtagEntity] = []
    user_mentions: list[UserMentionEntity] = Field(default=[], alias="user_mentions")

    model_config = ConfigDict(populate_by_name=True)


class UserEntities(BaseModel):
    """Entities attached to a user's profile (bio/description and url field)"""

    description: ProfileFieldEntities = ProfileFieldEntities()
    url: ProfileFieldEntities = ProfileFieldEntities()


class ProfileBio(BaseModel):
    """A user's expanded profile bio/description"""

    description: str = ""
    entities: dict[str, Any] = {}


class TwitterUser(BaseModel):
    """A twitter/X user, e.g. a tweet's author"""

    type: str
    id: str
    user_name: str = Field(alias="userName")
    name: str
    url: str
    twitter_url: str = Field(alias="twitterUrl")
    is_verified: bool = Field(alias="isVerified")
    is_blue_verified: bool = Field(alias="isBlueVerified")
    verified_type: str | None = Field(default=None, alias="verifiedType")
    profile_picture: str = Field(default="", alias="profilePicture")
    cover_picture: str = Field(default="", alias="coverPicture")
    description: str = ""
    location: str = ""
    followers: int = 0
    following: int = 0
    status: str = ""
    can_dm: bool = Field(default=False, alias="canDm")
    can_media_tag: bool = Field(default=False, alias="canMediaTag")
    created_at: str = Field(alias="createdAt")
    entities: UserEntities = UserEntities()
    fast_followers_count: int = Field(default=0, alias="fastFollowersCount")
    favourites_count: int = Field(default=0, alias="favouritesCount")
    has_custom_timelines: bool = Field(default=False, alias="hasCustomTimelines")
    is_translator: bool = Field(default=False, alias="isTranslator")
    media_count: int = Field(default=0, alias="mediaCount")
    statuses_count: int = Field(default=0, alias="statusesCount")
    withheld_in_countries: list[str] = Field(default=[], alias="withheldInCountries")
    possibly_sensitive: bool = Field(default=False, alias="possiblySensitive")
    pinned_tweet_ids: list[str] = Field(default=[], alias="pinnedTweetIds")
    profile_bio: ProfileBio | None = Field(default=None, alias="profile_bio")
    is_automated: bool = Field(default=False, alias="isAutomated")
    automated_by: str | None = Field(default=None, alias="automatedBy")

    model_config = ConfigDict(populate_by_name=True)


class TweetEntities(BaseModel):
    """Entities (hashtags, urls, mentions, symbols) extracted from a tweet's text"""

    hashtags: list[HashtagEntity] = []
    symbols: list[Any] = []
    urls: list[UrlEntityDetail] = []
    user_mentions: list[UserMentionEntity] = Field(default=[], alias="user_mentions")

    model_config = ConfigDict(populate_by_name=True)


class MediaSize(BaseModel):
    """Dimensions of a rendered variant of a media item, e.g. 'large'"""

    h: int
    w: int


class OriginalInfo(BaseModel):
    """The original (un-cropped) dimensions of a media item"""

    height: int
    width: int
    focus_rects: list[dict[str, int]] = Field(default=[], alias="focus_rects")

    model_config = ConfigDict(populate_by_name=True)


class Media(BaseModel):
    """A photo/video/gif attached to a tweet"""

    type: str
    media_key: str = Field(alias="media_key")
    id_str: str = Field(alias="id_str")
    url: str
    display_url: str = Field(alias="display_url")
    expanded_url: str = Field(alias="expanded_url")
    media_url_https: str = Field(alias="media_url_https")
    sizes: dict[str, MediaSize] = {}
    original_info: OriginalInfo | None = Field(default=None, alias="original_info")
    indices: list[int] = []
    ext_media_availability: dict[str, Any] = Field(
        default={}, alias="ext_media_availability"
    )

    model_config = ConfigDict(populate_by_name=True)


class ExtendedEntities(BaseModel):
    """Media entities attached to a tweet, keyed separately from `entities`"""

    media: list[Media] = []


class BoundingBoxPolygon(BaseModel):
    """The polygon describing a place's boundary"""

    type: str | None = None
    coordinates: list[Any] = []


class Place(BaseModel):
    """A geographic place tagged on a tweet"""

    id: str | None = None
    name: str | None = None
    full_name: str | None = Field(default=None, alias="full_name")
    country: str | None = None
    country_code: str | None = Field(default=None, alias="country_code")
    place_type: str | None = Field(default=None, alias="place_type")
    bounding_box_polygon: BoundingBoxPolygon | None = Field(
        default=None, alias="bounding_box_polygon"
    )

    model_config = ConfigDict(populate_by_name=True)


class CardBindingValue(BaseModel):
    """A single key/value pair describing part of a tweet's link-preview card"""

    key: str
    value: dict[str, Any] = {}


class Card(BaseModel):
    """A link-preview card (e.g. article summary) attached to a tweet"""

    name: str | None = None
    url: str | None = None
    binding_values: list[CardBindingValue] = Field(default=[], alias="binding_values")
    card_platform: dict[str, Any] | None = Field(default=None, alias="card_platform")
    user_refs_results: list[Any] = Field(default=[], alias="user_refs_results")

    model_config = ConfigDict(populate_by_name=True)


class TweetResult(BaseModel):
    """A single tweet (twitter/X post), as returned by the twitter API"""

    type: str
    id: str
    url: str
    twitter_url: str = Field(alias="twitterUrl")
    text: str
    source: str
    retweet_count: int = Field(default=0, alias="retweetCount")
    reply_count: int = Field(default=0, alias="replyCount")
    like_count: int = Field(default=0, alias="likeCount")
    quote_count: int = Field(default=0, alias="quoteCount")
    view_count: int = Field(default=0, alias="viewCount")
    created_at: str = Field(alias="createdAt")
    lang: str | None = None
    bookmark_count: int = Field(default=0, alias="bookmarkCount")
    is_reply: bool = Field(default=False, alias="isReply")
    in_reply_to_id: str | None = Field(default=None, alias="inReplyToId")
    conversation_id: str | None = Field(default=None, alias="conversationId")
    display_text_range: list[int] = Field(default=[], alias="displayTextRange")
    in_reply_to_user_id: str | None = Field(default=None, alias="inReplyToUserId")
    in_reply_to_username: str | None = Field(default=None, alias="inReplyToUsername")
    author: TwitterUser | None = None
    extended_entities: ExtendedEntities = Field(
        default=ExtendedEntities(), alias="extendedEntities"
    )
    card: Card | None = None
    place: Place | None = None
    entities: TweetEntities = TweetEntities()
    quoted_tweet: TweetResult | None = Field(default=None, alias="quoted_tweet")
    retweeted_tweet: TweetResult | None = Field(default=None, alias="retweeted_tweet")
    is_limited_reply: bool = Field(default=False, alias="isLimitedReply")
    community_info: dict[str, Any] | None = Field(default=None, alias="communityInfo")
    article: dict[str, Any] | None = None

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("author", mode="before")
    @classmethod
    def _empty_author_to_none(cls, value: Any) -> Any:
        """The API represents an unavailable quoted/retweeted tweet's author as `{}`"""
        return None if value == {} else value


class TweetSearchResult(BaseModel):
    """The top-level shape of a saved twitter API search response, e.g. the local json files"""

    tweets: list[TweetResult] = []


class TweetMinimal(BaseModel):
    """
    A scaled down version of the tweet that has just the internal id and the text of the post
    """

    id: int
    text: str


class TweetSentiment(BaseModel):
    """
    A tweet and the sentiment assigned to it.
    """

    id: int
    text: str
    sentiment: SentimentEnum


class TweetSentimentList(BaseModel):
    """
    A list of tweets and the sentiment assigned to each
    """

    tweets: List[TweetSentiment]


TweetResult.model_rebuild()
