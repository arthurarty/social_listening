from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


class NewsPage(SQLModel, table=True):
    """
    Represents a single news page
    """

    id: int | None = Field(default=None, primary_key=True)
    file_name: str
    file_path: str
    news_paper_name: str
    page_number: int
    date_published: datetime
    article_json: list[dict] | None = Field(default=None, sa_column=Column(JSONB))
    processed: bool = Field(default=False)
