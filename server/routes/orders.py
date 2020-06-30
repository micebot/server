from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from server.db import open_session
from server.db.repo import orders as repo
from server.models import schemas

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
    db: Session = Depends(open_session),
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
    "/",
    summary="Register a new order.",
    response_model=schemas.Order,
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    order: schemas.OrderCreation, db: Session = Depends(open_session)
):
    if repo.get_order_by_product_id(db=db, product_id=order.product_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The product id is already in use by another order.",
        )

    return repo.create_order(db=db, order=order)


@router.put(
    "/take/{order_id}",
    summary="Update an order to mark as taken.",
    response_model=schemas.Order,
    status_code=status.HTTP_200_OK,
)
def take_order(
    order_id: int, db: Session = Depends(open_session),
):
    if order := repo.get_order_by_id(db=db, order_id=order_id):
        return repo.take_order(db=db, order=order)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No order found for the id specified.",
    )
