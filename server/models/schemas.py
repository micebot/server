from datetime import datetime

from pydantic import BaseModel


class ProductBase(BaseModel):
    """The base properties of a product."""

    code: str
    summary: str = None


class ProductCreation(ProductBase):
    """The properties used to create a new product."""

    ...


class ProductUpdate(ProductBase):
    """The properties used to update a product."""

    ...


class Product(ProductBase):
    """The product schema exposed by the API."""

    id: int
    taken: bool = False
    taken_at: datetime = None

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    """The base properties of an order."""

    mod_id: str
    mod_display_name: str
    owner_display_name: str


class OrderCreation(OrderBase):
    """The properties used to create a new order."""

    ...


class Order(OrderBase):
    """The order schema exposed by the API."""

    id: int
    requested_at: datetime
    product: Product

    class Config:
        orm_mode = True
