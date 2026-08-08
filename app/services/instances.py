from app.services.news_page_service import NewsPageServiceImpl, NewsPageServiceInterface

news_page_service: NewsPageServiceImpl = NewsPageServiceImpl()


def get_news_page_service() -> NewsPageServiceInterface:
    """
    Returns the instance of the news_page_service that implements
    the NewsPageServiceInterface
    """
    return news_page_service
