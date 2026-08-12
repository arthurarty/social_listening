from abc import ABC, abstractmethod
from typing import List

from sqlmodel import Session, select

from app.database.models.topics import Topic


class TopicServiceInterface(ABC):
    """
    Interface for managing topics.
    """

    @abstractmethod
    def get_topics(
        self, session: Session, skip: int = 0, limit: int = 20
    ) -> List[Topic]:
        """
        Queries database for a list of topics
        """

    @abstractmethod
    def store_topic(self, session: Session, topic: Topic) -> int | None:
        """
        Persist topic to the database
        """


class TopicServiceImpl(TopicServiceInterface):
    """
    A service to manage topics.
    """

    def get_topics(
        self, session: Session, skip: int = 0, limit: int = 20
    ) -> List[Topic]:
        """
        Queries database for a list of topics
        """
        statement = select(Topic).order_by(Topic.id).offset(skip).limit(limit)
        return list(session.exec(statement).all())

    def store_topic(self, session: Session, topic: Topic) -> int | None:
        """
        Persist topic to the database. If a topic with the same name
        already exists, its description and examples are updated instead.
        """
        existing = session.exec(select(Topic).where(Topic.name == topic.name)).first()

        if existing:
            existing.description = topic.description
            existing.examples = topic.examples
            session.add(existing)
            session.commit()
            session.refresh(existing)
            return existing.id

        session.add(topic)
        session.commit()
        session.refresh(topic)
        return topic.id
