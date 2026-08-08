from datetime import datetime
from typing import Annotated, List

from fastapi import APIRouter, Form, HTTPException, Query, UploadFile, status

from app.dependencies import NewsPageServiceDep
from app.schemas.news_page_schemas import NewsPageCreationRequest, NewsPageRead

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


@router.get("/", response_model=List[NewsPageRead])
def list_news_pages(
    news_page_service: NewsPageServiceDep,
    processed: bool = False,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
):
    """
    Lists news pages, optionally filtered by processed status
    """
    return news_page_service.get_news_pages(processed=processed, skip=skip, limit=limit)
