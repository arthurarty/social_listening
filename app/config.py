from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Social Listening"
    database_url: str
    tweet_api_io: str
    # TWEETAPIIO
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
