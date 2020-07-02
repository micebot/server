from typing import Optional

from sqlalchemy.orm import Session

from server.db import entities


def get_app_by_uname(
    db: Session, uname: str
) -> Optional[entities.Application]:
    """
    Get an application by the username.

    Args:
        - db: the database session.
        - uname: the username.

    Returns:
        - None if no application was found for the username provided,
        otherwise application object is returned.
    """
    return db.query(entities.Application).filter_by(username=uname).first()


def auth_application(
    db: Session, uname: str, password: str
) -> Optional[entities.Application]:
    """
    Authenticate the application.

    Args:
        - db: the database session.
        - uname: the username for app.
        - password: the password for app.

    Returns:
        - None if the authentication fails, otherwise the application
        object is returned.
    """
    if app := get_app_by_uname(db=db, uname=uname):
        if app.check_password(plain_password=password):
            return app
    return None
