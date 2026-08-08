import uuid
from abc import ABC, abstractmethod
from pathlib import Path

import aiofiles

from app.config import settings
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
        return "Done"
