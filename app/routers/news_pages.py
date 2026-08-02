from fastapi import APIRouter, UploadFile, status, HTTPException
import aiofiles
import uuid
from pathlib import Path


UPLOAD_DIR = Path("local_files/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
ALLOWED_TYPES = {"image/jpeg", "image/png"}
MAX_SIZE = 10 * 1024 * 1024  # 10MB


router = APIRouter(
    prefix="/news-pages",
    tags=["news_pages"]
)


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
        raise HTTPException(status.HTTP_413_CONTENT_TOO_LARGE, "File too large")
    if not file.filename:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Could not name file.")
    ext = Path(file.filename).suffix
    safe_name = f"{uuid.uuid4()}{ext}"
    dest = UPLOAD_DIR / safe_name

    async with aiofiles.open(dest, "wb") as out_file:
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break
            await out_file.write(chunk)
    return {
        "message": f"Page: {file.filename} scan uploaded"
    }
