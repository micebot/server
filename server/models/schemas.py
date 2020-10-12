from datetime import datetime
from typing import List

from pydantic import BaseModel, UUID4


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

    uuid: UUID4
    taken: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ProductDelete(BaseModel):
    """The responde schema for a product deletion."""

    deleted: bool


class ProductCount(BaseModel):
    """The product counter statistics."""

    all: int
    taken: int
    available: int


class ProductWithTotal(BaseModel):
    """The total product counter with the products entities."""

    total: ProductCount
    products: List[Product] = []


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

    uuid: UUID4
    requested_at: datetime
    product: Product

    class Config:
        orm_mode = True


class OrderWithTotal(BaseModel):
    """The total orders counter with the orders entities."""

    total: int
    orders: List[Order]


class HeartBeat(BaseModel):
    """The schema for heartbeat verification."""

    valid: bool
