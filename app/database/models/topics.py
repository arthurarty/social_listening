from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


class Topic(SQLModel, table=True):
    """
    User posts will be grouped into topics.
    This table stores the various topics we have.
    """

    __tablename__ = "topics"  # type: ignore[assignment]

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    description: str
    examples: list[str] = Field(default=None, sa_column=Column(JSONB))
