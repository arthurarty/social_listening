from fastapi import APIRouter, UploadFile, status


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
    return {
        "message": f"Page: {file.filename} scan uploaded"
    }
