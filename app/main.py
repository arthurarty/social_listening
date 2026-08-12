from fastapi import FastAPI

from app.routers import news_pages_router, topics_router

app = FastAPI()
app.include_router(news_pages_router.router)
app.include_router(topics_router.router)


@app.get("/")
async def root():
    return {"message": "Welcome to social listening"}
