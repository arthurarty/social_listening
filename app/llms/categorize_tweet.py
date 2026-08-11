"""
Categorize a tweet.
"""

from app.services.instances import twitter_service


def main(no_of_tweets: int = 3):
    """
    Read tweets from the database and assign them into categories.
    The categories exist in the categories table.
    """
    tweets = twitter_service.get_tweets_minimal(tweet_lang="en", limit=no_of_tweets)
    print(tweets)
