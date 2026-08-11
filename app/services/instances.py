from app.services.category_service import CategoryServiceImpl, CategoryServiceInterface
from app.services.news_page_service import NewsPageServiceImpl, NewsPageServiceInterface
from app.services.twitter_service import TwitterServiceImpl

news_page_service: NewsPageServiceImpl = NewsPageServiceImpl()
twitter_service: TwitterServiceImpl = TwitterServiceImpl()
category_service: CategoryServiceImpl = CategoryServiceImpl()


def get_category_service() -> CategoryServiceInterface:
    """
    Returns the instance of the category_service that implements the CategoryInterface.
    """
    return category_service


def get_news_page_service() -> NewsPageServiceInterface:
    """
    Returns the instance of the news_page_service that implements
    the NewsPageServiceInterface
    """
    return news_page_service
