from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from server.env import env


def open_session() -> Iterator[Session]:
    """Get a session from database connection."""
    try:
        db = sessionmaker(
            bind=create_engine(env.database_url),
            autocommit=False,
            autoflush=False,
        )()
        yield db
    finally:
        db.close()  # noqa
