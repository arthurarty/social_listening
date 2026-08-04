from fastapi import FastAPI

from app.routers import news_pages_router

app = FastAPI()
app.include_router(news_pages_router.router)


@app.get("/")
async def root():
    return {"message": "Welcome to social listening"}
