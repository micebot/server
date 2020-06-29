from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Entity(Base):
    __abstract__ = True
    id = Column(Integer, nullable=False, primary_key=True, index=True)


class Product(Entity):
    __tablename__ = "product"
    code = Column(String, nullable=False, unique=True, index=True)
    summary = Column(String, nullable=False)
    taken = Column(Boolean, nullable=False, default=False)
    taken_at = Column(DateTime, nullable=True)

    def __repr__(self):  # pragma: no cover
        return str(self.__dict__)


class Order(Entity):  # pragma: no cover
    __tablename__ = "order"
    mod_id = Column(String, nullable=False)
    mod_display_name = Column(String, nullable=False)
    owner_display_name = Column(String, nullable=False)
    requested_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    product = relationship("Product")

    def __repr__(self):
        return str(self.__dict__)
