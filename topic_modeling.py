import re

from app.services.instances import twitter_service

MENTION_OR_HASHTAG_PATTERN = re.compile(r"[@#]\w+")
EMOJI_PATTERN = re.compile(
    "["
    "\U0001f300-\U0001faff"  # symbols & pictographs, extended-A
    "\U0001f1e6-\U0001f1ff"  # regional indicators (flags)
    "\U00002600-\U000027bf"  # misc symbols & dingbats
    "\U0001f000-\U0001f0ff"  # mahjong/cards/dominoes
    "\U00002300-\U000023ff"  # misc technical (e.g. watches)
    "\U0000fe0f"  # variation selector
    "]+",
    flags=re.UNICODE,
)


def clean_tweet(tweet: str) -> str:
    """
    Clean the tweet by removing icons, emojis, hashtags and tags
    """
    tweet = MENTION_OR_HASHTAG_PATTERN.sub("", tweet)
    tweet = EMOJI_PATTERN.sub("", tweet)
    return re.sub(r"\s+", " ", tweet).strip()


def main():
    tweets = twitter_service.get_tweets_as_text(limit=10)
    cleaned_tweets = [clean_tweet(tweet) for tweet in tweets]
    print(cleaned_tweets)


main()
