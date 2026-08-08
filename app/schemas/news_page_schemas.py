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


class NewsPageRead(BaseModel):
    """
    Schema for returning a news page
    """

    id: int
    file_name: str
    file_path: str
    news_paper_name: str
    page_number: int
    date_published: datetime
    processed: bool

    class Config:
        from_attributes = True
