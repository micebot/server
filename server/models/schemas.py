from datetime import datetime  # pragma: no cover

from pydantic import BaseModel  # pragma: no cover


class ProductBase(BaseModel):  # pragma: no cover
    code: str
    summary: str = None


class ProductCreation(ProductBase):  # pragma: no cover
    ...


class Product(ProductBase):  # pragma: no cover
    id: int
    taken: bool = False
    taken_at: datetime = None

    class Config:
        orm_mode = True


class OrderBase(BaseModel):  # pragma: no cover
    mod_id: str
    mod_display_name: str
    owner_display_name: str
    requested_at: datetime


class OrderCreation(OrderBase):  # pragma: no cover
    product_id: int


class Order(OrderBase):  # pragma: no cover
    id: int
    product: Product

    class Config:
        orm_mode = True
