from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, UploadFile, status

from app.dependencies import NewsPageServiceDep
from app.schemas.news_page_schemas import NewsPageCreationRequest

ALLOWED_TYPES = {"image/jpeg", "image/png"}
MAX_SIZE = 10 * 1024 * 1024  # 10MB


router = APIRouter(prefix="/news-pages", tags=["news_pages"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def uploads_news_page(
    news_paper_name: Annotated[str, Form()],
    page_number: Annotated[int, Form()],
    date_published: Annotated[datetime, Form()],
    file: UploadFile,
    news_page_service: NewsPageServiceDep,
):
    """
    Uploads an image of a news paper page
    """
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Unsupported file type")
    if (not file.size) or file.size > MAX_SIZE:
        raise HTTPException(status.HTTP_413_CONTENT_TOO_LARGE, "File too large")
    if not file.filename:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Could not name file.")

    output = await news_page_service.create_news_page(
        NewsPageCreationRequest(
            page_number=page_number,
            date_published=date_published,
            file=file,
            news_paper_name=news_paper_name,
        )
    )
    return {"message": f"{output}"}
