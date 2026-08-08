from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Social Listening"
    file_upload_dir: str = "local_files/uploads"
    database_url: str
    tweet_api_io: str
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
