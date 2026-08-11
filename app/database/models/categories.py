from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


class Category(SQLModel, table=True):
    """
    Represents a category that a tweet or post belongs to
    """

    __tablename__ = "categories"  # type: ignore[assignment]

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    description: str
    examples: list[str] = Field(default=None, sa_column=Column(JSONB))
