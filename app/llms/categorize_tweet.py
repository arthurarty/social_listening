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
1. A list of categories, each with an id, name, description, and examples.
2. A list of tweets to categorize, each with an id and text.

Your task:
- Assign exactly one category to each tweet from the provided category list only.
  Never invent a category that is not in the list.
- Base your decision on the tweet's substantive content. Ignore noise such as
  URLs, mentions, and hashtags unless they carry meaning relevant to the categories.
- Use each category's description and examples to judge fit, not just its name.
- If a tweet could reasonably fit multiple categories, choose the single best match.
  If none fit well, choose the closest one — every tweet must be assigned.
- For each tweet, copy tweet_id and tweet_text exactly as given.
- For the assigned category, copy category_id and category_name exactly as given
  in the category list — do not alter, translate, or reformat them.
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
