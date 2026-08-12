from app.services.news_page_service import NewsPageServiceImpl, NewsPageServiceInterface
from app.services.topic_service import TopicServiceImpl, TopicServiceInterface
from app.services.twitter_service import TwitterServiceImpl

news_page_service: NewsPageServiceImpl = NewsPageServiceImpl()
twitter_service: TwitterServiceImpl = TwitterServiceImpl()
topic_service: TopicServiceImpl = TopicServiceImpl()


def get_topic_service() -> TopicServiceInterface:
    """
    Returns the instance of the topic_service that implements the TopicServiceInterface.
    """
    return topic_service


def get_news_page_service() -> NewsPageServiceInterface:
    """
    Returns the instance of the news_page_service that implements
    the NewsPageServiceInterface
    """
    return news_page_service
