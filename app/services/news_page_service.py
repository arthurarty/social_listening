import uuid
from abc import ABC, abstractmethod
from pathlib import Path

import aiofiles

from app.config import settings
from app.database.connection import db_session
from app.database.news_page import NewsPage
from app.schemas.news_page_schemas import NewsPageCreationRequest

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
