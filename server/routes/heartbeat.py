from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from server.models import schemas
from server.models.oauth2 import auth

router = APIRouter()


@router.get(
    "/",
    summary="Check if the application and authentication code is valid.",
    status_code=status.HTTP_200_OK,
    response_model=schemas.HeartBeat,
)
def heartbeat(_: Session = Depends(auth)):
    """Check if code/app is valid."""
    return {"valid": True}
