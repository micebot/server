from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Session

from server.db import entities
from server.models import schemas


def get_orders(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    moderator: str = None,
    owner: str = None,
    taken: bool = False,
) -> Optional[List[entities.Order]]:
    """
    Get the registed orders using filters.

    Args:
        - db: the database session.
        - skip: the number of filtered entities to skip.
        - limit: the number of entities to limit the query.
        - moderadtor: the moderator name that create the order.
        - owner: the owner name that receive the order.
        - taken: filter orders that have already taken or not.

    Returns:
        - the list of orders or `None` if there are no orders to return
        using the filter specified.
    """
    query = db.query(entities.Order)

    if moderator:
        query = query.filter_by(mod_display_name=moderator)

    if owner:
        query = query.filter_by(owner_display_name=owner)

    return (
        query.join(entities.Product)
        .filter(entities.Product.taken == taken)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_order_by_product_code(
    db: Session, code: str
) -> Optional[entities.Order]:
    """
    Get an order by the product code.

    Args:
        - db: the database session.
        - code: the product code.

    Returns:
        - None if no product was found for the provided code, otherwise
        the order containing the product is returned.
    """
    return (
        db.query(entities.Order)
        .join(entities.Product)
        .filter(entities.Product.code == code)
        .first()
    )


def create_order_for_product(
    db: Session, product: entities.Product, order: schemas.OrderCreation
) -> entities.Order:
    """
    Create a new order and mark the product as taken.

    Args:
        - db: the database session.
        - product: the product to be used on order.
        - order: the order schema.

    Returns:
        - the order created with product marked as taken.
    """

    product.taken = True
    product.taken_at = datetime.utcnow()

    db_order = entities.Order(**order.dict())
    db_order.product = product
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order
