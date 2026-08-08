from pydantic import BaseModel


class Article(BaseModel):
    """
    A single article extracted from a news page
    """

    headline: str
    body: str
    author: str | None
