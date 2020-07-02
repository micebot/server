from typing import Optional

from sqlalchemy.orm import Session

from server.db import entities


def get_app_by_uname(
    db: Session, uname: str
) -> Optional[entities.Application]:
    return db.query(entities.Application).filter_by(username=uname).first()


def auth_application(
    db: Session, uname: str, password: str
) -> Optional[entities.Application]:

    if app := get_app_by_uname(db=db, uname=uname):
        if app.check_password(plain_password=password):
            return app
    return None
