from app.schemas.article_schema import Article
from app.services.instances import news_page_service

articles = [
    Article(
        headline="Uganda airlines to Kigali",
        body="Uganda Airlines will be flying to kigali",
        author="Jack Ma",
    )
]


news_pages = news_page_service.get_news_pages()
print(news_pages)

news_page_service.update_news_page_articles(news_page_id=1, articles=articles)
