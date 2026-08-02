from datetime import datetime

from sqlmodel import Field, SQLModel


class NewsPage(SQLModel, table=True):
    """
    Represents a single news page
    """

    id: int | None = Field(default=None, primary_key=True)
    file_name: str
    news_paper_name: str
    page_number: int
    date_published: datetime
    processed: bool = Field(default=False)
