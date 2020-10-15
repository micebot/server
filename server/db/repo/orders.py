from typing import List, Optional

from sqlalchemy.orm import Session

from server.db import entities
from server.models import schemas


def get_orders(
    db: Session,
    skip: int = 0,
    limit: int = 50,
    moderator: str = None,
    owner: str = None,
    desc: bool = True,
) -> Optional[List[entities.Order]]:
    """
    Get the registed orders using filters.

    Args:
        - db: the database session.
        - skip: the number of filtered entities to skip.
        - limit: the number of entities to limit the query.
        - moderadtor: the moderator name that create the order.
        - owner: the owner name that receive the order.
        - desc: order by request_at datetime.

    Returns:
        - the list of orders or `None` if there are no orders to return
        using the filter specified.
    """
    order_by = (
        entities.Order.requested_at.desc()
        if desc
        else entities.Order.requested_at.asc()
    )

    query = db.query(entities.Order).order_by(order_by)

    if moderator:
        query = query.filter_by(mod_display_name=moderator)

    if owner:
        query = query.filter_by(owner_display_name=owner)

    return query.offset(skip).limit(limit).all()


def get_orders_count(db: Session) -> int:
    """Return the number of entities from orders table."""
    return db.query(entities.Order).count()


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

    db_order = entities.Order(**order.dict())
    db_order.product = product
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order
