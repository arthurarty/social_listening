from typing import List

from pydantic import BaseModel


class Article(BaseModel):
    """
    A single article extracted from a news page
    """

    headline: str
    body: str
    author: str | None


class ArticleList(BaseModel):
    """
    A list of articles found on a news page
    """

    articles: List[Article]
