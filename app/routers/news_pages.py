from fastapi import APIRouter, UploadFile, status, HTTPException
import aiofiles
import uuid
from pathlib import Path


router = APIRouter(
    prefix="/news-pages",
    tags=["news_pages"]
)


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
ALLOWED_TYPES = {"image/jpeg", "image/png"}
MAX_SIZE = 10 * 1024 * 1024  # 10MB


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
async def uploads_news_page(file: UploadFile):
    """
    Uploads an image of a news paper page
    """
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Unsupported file type"
        )
    if (not file.size) or file.size > MAX_SIZE:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "File too large")
    return {
        "message": f"Page: {file.filename} scan uploaded"
    }
