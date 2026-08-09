import uuid
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

import aiofiles
from sqlalchemy import update
from sqlmodel import select

from app.config import settings
from app.database.connection import db_session
from app.database.models.news_page import NewsPage
from app.schemas.article_schema import Article
from app.schemas.news_page_schemas import NewsPageCreationRequest, NewsPageRead

UPLOAD_DIR = Path(settings.file_upload_dir)
UPLOAD_DIR.mkdir(exist_ok=True)


class NewsPageServiceInterface(ABC):
    """
    The Page service will implement this interface.
    """

    @abstractmethod
    async def create_news_page(self, creation_request: NewsPageCreationRequest) -> str:
        """
        Creates a news page
        """

    @abstractmethod
    def get_news_pages(
        self, processed: bool = False, skip: int = 0, limit: int = 10
    ) -> List[NewsPageRead]:
        """
        Get news pages
        """

    @abstractmethod
    def update_news_page_articles(
        self, news_page_id: int, articles: List[Article]
    ) -> None:
        """
        Update the articles field of a news page.
        """


class NewsPageServiceImpl(NewsPageServiceInterface):
    """
    Implementation of the news page service interface
    """

    def __init__(self) -> None:
        pass

    async def create_news_page(self, creation_request: NewsPageCreationRequest) -> str:
        """
        Creates a news page
        """
        file = creation_request.file
        if not file.filename:
            raise ValueError("File name not found")
        ext = Path(file.filename).suffix
        safe_name = f"{uuid.uuid4()}{ext}"
        dest = UPLOAD_DIR / safe_name

        async with aiofiles.open(dest, "wb") as out_file:
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break
                await out_file.write(chunk)
        news_page = NewsPage(
            file_name=str(file.filename),
            file_path=str(dest),
            news_paper_name=creation_request.news_paper_name,
            page_number=creation_request.page_number,
            date_published=creation_request.date_published,
        )
        with db_session() as session:
            session.add(news_page)
        return "Done"

    def get_news_pages(
        self, processed: bool = False, skip: int = 0, limit: int = 10
    ) -> List[NewsPageRead]:
        with db_session() as session:
            query = (
                select(NewsPage)
                .where(NewsPage.processed == processed)
                .limit(limit)
                .order_by(NewsPage.id)
                .offset(skip)
            )
            news_pages = session.execute(query).scalars().all()
            return [NewsPageRead.model_validate(news_page) for news_page in news_pages]

    def update_news_page_articles(
        self, news_page_id: int, articles: List[Article]
    ) -> None:
        """
        Update the articles field of a news page. Method overwrites the existing articles
        """
        article_dicts = [article.model_dump() for article in articles]
        with db_session() as session:
            query = (
                update(NewsPage)
                .where(NewsPage.id == news_page_id)
                .values(article_json=article_dicts)
            )
            session.execute(query)
        return None
