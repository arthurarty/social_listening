from fastapi import APIRouter


router = APIRouter(
    prefix="/news-pages",
    tags=["news_pages"]
)


@router.post("/")
async def uploads_news_page():
    """
    Uploads an image of a news paper page
    """
    return {
        "message": "Page scan uploaded"
    }
