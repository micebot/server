from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from server.env import env


def open_session() -> Iterator[Session]:
    """Get a session from database connection."""
    try:
        connect_args = (
            {"check_same_thread": False}
            if env.database_url.startswith("sqlite")
            else {}
        )

        db = sessionmaker(
            bind=create_engine(env.database_url, connect_args=connect_args),
            autocommit=False,
            autoflush=False,
        )()
        yield db
    finally:
        db.close()  # noqa
