from fastapi import APIRouter, Depends, security, HTTPException, status
from sqlalchemy.orm import Session

from server.db import open_session
from server.db.repo.apps import auth_application
from server.models.oauth2 import create_access_token

router = APIRouter()

auth_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate your credentials.",
)


@router.post("/", summary="Authentication")
async def authenticate(
    form: security.OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(open_session),
):
    """Authenticate the application to consume our API."""
    app = auth_application(db=db, uname=form.username, password=form.password)

    if not app:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or unknown client application.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "access_token": create_access_token(data={"sub": app.username}),
        "token_type": "bearer",
    }
