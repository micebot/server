from datetime import datetime
from typing import NoReturn

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from server.models.security import pw_context

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


class Order(Entity):
    __tablename__ = "order"
    mod_id = Column(String, nullable=False)
    mod_display_name = Column(String, nullable=False)
    owner_display_name = Column(String, nullable=False)
    requested_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    product = relationship("Product")

    def __repr__(self):  # pragma: no cover
        return str(self.__dict__)


class Application(Entity):
    __tablename__ = "application"
    username = Column(String, nullable=False, unique=True)
    pass_hash = Column(String, nullable=False)

    @hybrid_property
    def password(self):
        return self.pass_hash

    @password.setter
    def password(self, plain_password: str) -> NoReturn:  # pragma: no cover
        self.pass_hash = pw_context.hash(plain_password)

    def check_password(self, plain_password: str) -> bool:  # pragma: no cover
        return pw_context.verify(plain_password, self.pass_hash)

    def __repr__(self):  # pragma: no cover
        return str(self.__dict__)
