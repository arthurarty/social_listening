from datetime import datetime

from fastapi import UploadFile
from pydantic import BaseModel


class NewsPageCreationRequest(BaseModel):
    """
    Schema for request to create news page
    """

    page_number: int
    news_paper_name: str
    date_published: datetime
    file: UploadFile
    file_name: str
