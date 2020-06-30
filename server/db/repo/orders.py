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
        query.filter(entities.Product.taken == taken)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_order_by_id(db: Session, order_id: int) -> Optional[entities.Order]:
    return db.query(entities.Order).filter_by(id=order_id).first()


def get_order_by_product_id(
    db: Session, product_id: int
) -> Optional[entities.Order]:
    return db.query(entities.Order).filter_by(product_id=product_id).first()


def create_order(db: Session, order: schemas.OrderCreation) -> entities.Order:
    db_order = entities.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def take_order(db: Session, order: entities.Order) -> entities.Order:
    order.product.taken = True
    order.product.taken_at = datetime.utcnow()
    db.commit()
    return order
