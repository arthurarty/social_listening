from abc import ABC, abstractmethod


class NewsPageServiceInterface(ABC):
    """
    The Page service will implement this interface.
    """

    @abstractmethod
    def create_news_page(self):
        """
        Creates a news page
        """


class NewsPageServiceImpl(NewsPageServiceInterface):
    """
    Implementation of the news page service interface
    """

    def __init__(self) -> None:
        pass

    def create_news_page(self):
        """
        Creates a news page
        """
