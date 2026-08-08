from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, create_engine

from app.config import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine)


def get_session():
    """
    Yields a session, used with FastAPI dependency injection
    """
    with Session(engine) as session:
        yield session


@contextmanager
def db_session(commit: bool = True):
    """
    Provide a transactional scope around a series of operations.
    Use this when you managing the lifecycle of session manually.
    """
    session = SessionLocal()
    try:
        yield session
        if commit:
            session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
