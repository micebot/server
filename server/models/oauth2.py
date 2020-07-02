from datetime import timedelta, datetime
from typing import Dict

from fastapi import HTTPException, security, status, Depends
from jwt import PyJWTError, decode, encode
from sqlalchemy.orm import Session

from server import env
from server.db import open_session
from server.db.repo.apps import get_app_by_uname

oauth_schema = security.OAuth2PasswordBearer(tokenUrl="/auth")

auth_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate your credentials.",
)


async def auth(
    token: str = Depends(oauth_schema), db: Session = Depends(open_session)
):
    try:
        uname = decode(
            token, env.secret_key, algorithms=[env.token_algorithm]
        ).get("sub")

        if not uname:
            raise auth_exception

    except PyJWTError:
        raise auth_exception

    app = get_app_by_uname(db=db, uname=uname)
    if not app:
        raise auth_exception

    return db


def create_access_token(
    *, data: Dict, expires_delta: timedelta = timedelta(minutes=20)
):
    data_to_encode = data.copy()
    data_to_encode.update({"exp": datetime.utcnow() + expires_delta})
    return encode(
        data_to_encode, env.secret_key, algorithm=env.token_algorithm
    )