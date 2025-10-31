from typing import Generator
from sqlmodel import create_engine, SQLModel, Session
from core.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    """
    Creates all database tables based on SQLModel metadata.
    This is called once on application startup.
    """

    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency to create and manage a database session
    for each request.
    """
    with Session(engine) as session:
        yield session
