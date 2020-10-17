from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from server.env import env

engine = create_engine(env.DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def open_session() -> Iterator[Session]:
    """Get a session from database connection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
