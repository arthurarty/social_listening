from fastapi import FastAPI

from app.routers import news_pages

app = FastAPI()
app.include_router(news_pages.router)


@app.get("/")
async def root():
    return {"message": "Welcome to social listening"}
