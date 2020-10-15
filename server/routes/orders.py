from fastapi import APIRouter, Depends, HTTPException, status
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
    response_model=schemas.OrderWithTotal,
)
def get_orders(
    skip: int = 0,
    limit: int = 50,
    moderator: str = None,
    owner: str = None,
    desc: bool = False,
    db: Session = Depends(auth),
):
    """Get all the orders."""
    entities = repo.get_orders(
        db=db,
        skip=skip,
        limit=limit,
        moderator=moderator,
        owner=owner,
        desc=desc,
    )

    return {"total": repo.get_orders_count(db=db), "orders": entities}


@router.post(
    "/{product_uuid}",
    summary="Generate a new order for a product.",
    response_model=schemas.Order,
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    product_uuid: str,
    order: schemas.OrderCreation,
    db: Session = Depends(auth),
):
    """Generate a new order for a product."""
    if product := product_repo.get_product_by_uuid(db=db, uuid=product_uuid):
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
        detail="No product found for the uuid provided.",
    )
