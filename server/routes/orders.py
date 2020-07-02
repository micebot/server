from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from server.db.repo import orders as repo
from server.db.repo import products as product_repo
from server.models import schemas
from server.models.oauth2 import auth

router = APIRouter()


@router.get(
    "/",
    summary="Get all the orders.",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.Order],
)
def get_orders(
    skip: int = 0,
    limit: int = 50,
    moderator: str = None,
    owner: str = None,
    taken: bool = False,
    db: Session = Depends(auth),
):
    if entities := repo.get_orders(
        db=db,
        skip=skip,
        limit=limit,
        moderator=moderator,
        owner=owner,
        taken=taken,
    ):
        return entities

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No orders registered yet.",
    )


@router.post(
    "/{code}",
    summary="Generate a new order for a product.",
    response_model=schemas.Order,
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    code: str, order: schemas.OrderCreation, db: Session = Depends(auth),
):
    if product := product_repo.get_product_by_code(db=db, code=code):
        if product.taken:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="The product code is already taken.",
            )
        return repo.create_order_for_product(
            db=db, product=product, order=order
        )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No product found for the code provided.",
    )
