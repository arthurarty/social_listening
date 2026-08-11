"""
Categorize a tweet.
"""

from contextlib import contextmanager

from ollama import chat

from app.database.connection import get_session
from app.schemas.category_schema import CategorizedTweetsOutput, CategoryRead
from app.services.instances import category_service, twitter_service

SYSTEM_PROMPT = """
You are an expert at categorizing tweets.

You will be given:
1. A list of categories. Each category will have an id, name, description and examples.
2. A list of tweets to categorize. Each tweet will have an id and text of the tweet.

Your task:
- Assign a category to each tweet.
- Basing on the text of each tweet pick from the category list the most appropriate.
- When picking a category to assign a tweet, consider the description of the category and examples in that category.
- Your output will be the tweet_id, tweet_text, category_id, category_name.

"""


def main(no_of_tweets: int = 3, skip: int = 0):
    """
    Read tweets from the database and assign them into categories.
    The categories exist in the categories table.
    """
    with contextmanager(get_session)() as session:
        categories = category_service.get_categories(session)
        categories_data = [
            CategoryRead.model_validate(category).model_dump()
            for category in categories
        ]
    tweets = twitter_service.get_tweets_minimal(
        tweet_lang="en", limit=no_of_tweets, skip=skip
    )
    response = chat(
        model="gemma4",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": f"Categories: {categories_data}\n\nTweets: {tweets}",
            },
        ],
        format=CategorizedTweetsOutput.model_json_schema(),
        options={
            "temperature": 0,
            "seed": 42,
        },
    )

    if response.message.content is None:
        raise ValueError("Model returned an empty response")

    return CategorizedTweetsOutput.model_validate_json(response.message.content)
