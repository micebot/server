from typing import Optional, List, NoReturn

from sqlalchemy.orm import Session

from server.db import entities
from server.models import schemas


def get_products(
    db: Session, skip: int = 0, limit: int = 50, taken: bool = False
) -> Optional[List[entities.Product]]:
    """
    Get the registed products using filters.

    Args:
        - db: the database session.
        - skip: the number of filtered entities to skip.
        - limit: the number of entities to limit the query.
        - taken: filter by products that have already taken or not.

    Returns:
        - the list of products or `None` if there are no products to
        return using the filter specified.
    """
    return (
        db.query(entities.Product)
        .filter_by(taken=taken)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_product_by_code(db: Session, code: str) -> Optional[entities.Product]:
    """
    Get a specific product by the code.

    Args:
        - db: the database session.
        - code: the product code to be used in query.

    Returns:
        - the product object if it is found, otherwise `None` is returned.
    """
    return db.query(entities.Product).filter_by(code=code).first()


def create_product(
    db: Session, product: schemas.ProductCreation
) -> entities.Product:
    """
    Persit a new product.

    Args:
        - db: the database session.
        - product: the product schema.

    Returns:
        - the product object with generated values.
    """
    db_product = entities.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(
    db: Session, product: schemas.ProductUpdate, db_product: entities.Product
) -> entities.Product:
    """
    Update an existing product.

    Args:
        - db: the database session.
        - product: the product schema.
        - db_product: the product to be updated with `product` schema.

    Returns:
        - the updated product.
    """
    db_product.code = product.code

    if product.summary:
        db_product.summary = product.summary

    db.commit()
    return db_product


def delete_product(db: Session, product: entities.Product) -> NoReturn:
    """
    Remove an existing product.

    Args:
        - db: the database session.
        - product: the product to be deleted.
    """
    db.delete(product)
    db.commit()
