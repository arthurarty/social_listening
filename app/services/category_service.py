from abc import ABC, abstractmethod
from typing import List

from sqlmodel import Session, select

from app.database.models.categories import Category


class CategoryServiceInterface(ABC):
    """
    Interface for managing categories.
    """

    @abstractmethod
    def get_categories(
        self, session: Session, skip: int = 0, limit: int = 20
    ) -> List[Category]:
        """
        Queries database for a list of categories
        """

    @abstractmethod
    def store_category(self, session: Session, category: Category) -> int | None:
        """
        Persist category to the database
        """


class CategoryServiceImpl(CategoryServiceInterface):
    """
    A service to manage categories.
    """

    def get_categories(
        self, session: Session, skip: int = 0, limit: int = 20
    ) -> List[Category]:
        """
        Queries database for a list of categories
        """
        statement = select(Category).order_by(Category.id).offset(skip).limit(limit)
        return list(session.exec(statement).all())

    def store_category(self, session: Session, category: Category) -> int | None:
        """
        Persist category to the database. If a category with the same name
        already exists, its description and examples are updated instead.
        """
        existing = session.exec(
            select(Category).where(Category.name == category.name)
        ).first()

        if existing:
            existing.description = category.description
            existing.examples = category.examples
            session.add(existing)
            session.commit()
            session.refresh(existing)
            return existing.id

        session.add(category)
        session.commit()
        session.refresh(category)
        return category.id
