from datetime import datetime

from pydantic import BaseModel


class ProductBase(BaseModel):
    code: str
    summary: str = None


class ProductCreation(ProductBase):
    ...


class ProductUpdate(ProductBase):
    ...


class Product(ProductBase):
    id: int
    taken: bool = False
    taken_at: datetime = None

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    mod_id: str
    mod_display_name: str
    owner_display_name: str


class OrderCreation(OrderBase):
    ...


class Order(OrderBase):
    id: int
    requested_at: datetime
    product: Product

    class Config:
        orm_mode = True
