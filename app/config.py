import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]


class Settings(BaseSettings):
    app_name: str = "Social Listening"
    database_url: str
    tweet_api_io: str
    # TWEETAPIIO
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
