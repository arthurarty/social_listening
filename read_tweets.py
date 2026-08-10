import argparse
import json

from app.services.instances import twitter_service


def main(json_file_path: str):
    """
    Reads a json file and persists the tweets to the database.

    How to run:
    python read_tweets.py local_files/twitter_api/sun_9th_aug_uganda_1.json
    """
    with open(json_file_path, encoding="utf-8") as f:
        json_content = json.load(f)
    tweet_search_result = twitter_service.convert_json_to_pydantic_model(json_content)
    tweets = twitter_service.convert_tweet_search_results_to_db_model(
        tweet_search_result
    )
    twitter_service.store_tweets(tweets)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Read tweets from a json file into the database."
    )
    parser.add_argument(
        "json_file_path", help="Path to the json file containing tweets."
    )
    args = parser.parse_args()
    main(args.json_file_path)
