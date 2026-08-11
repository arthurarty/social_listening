from fastapi import FastAPI

from app.routers import categories_router, news_pages_router

app = FastAPI()
app.include_router(news_pages_router.router)
app.include_router(categories_router.router)


@app.get("/")
async def root():
    return {"message": "Welcome to social listening"}
