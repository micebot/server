from typing import NoReturn
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    sql,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from server.models.security import pw_context

Base = declarative_base()


class Entity(Base):
    """
    Represents a base entity.

    This adds a non nullable integer as primary key for models/entities
    that inherits from `Entity`. A index is also created too.
    """

    __abstract__ = True
    id = Column(Integer, nullable=False, primary_key=True, index=True)


class Product(Entity):
    """
    Represents a product entity.

    Contains the code to be redeemed.
    """

    __tablename__ = "product"
    uuid = Column(
        UUID(as_uuid=True), nullable=False, unique=True, default=uuid4
    )
    code = Column(String, nullable=False, unique=True, index=True)
    summary = Column(String, nullable=False)
    taken = Column(Boolean, nullable=False, default=sql.false())
    created_at = Column(
        DateTime, nullable=False, server_default=sql.func.now()
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=sql.func.now(),
        onupdate=sql.func.now(),
    )

    def __repr__(self):  # pragma: no cover
        return str(self.__dict__)


class Order(Entity):
    """
    Represents an order entity.

    Contains information from a code redemption request.
    Consider the information of the moderator who requested the code, the user
    who received it, general date/time information, and the product identifier.
    """

    __tablename__ = "order"
    uuid = Column(
        UUID(as_uuid=True), nullable=False, unique=True, default=uuid4
    )
    mod_id = Column(String, nullable=False)
    mod_display_name = Column(String, nullable=False)
    owner_display_name = Column(String, nullable=False)
    requested_at = Column(DateTime, nullable=False, default=sql.func.now())
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    product = relationship("Product")

    def __repr__(self):  # pragma: no cover
        return str(self.__dict__)


class Application(Entity):
    """
    Represents an application entity.

    We use it to define what applications can consume our API.
    """

    __tablename__ = "application"
    username = Column(String, nullable=False, unique=True)
    pass_hash = Column(String, nullable=False)

    @hybrid_property
    def password(self):
        """Retrieve the hashed password."""
        return self.pass_hash

    @password.setter  # noqa
    def password(self, plain_password: str) -> NoReturn:
        """
        Hash the password.

        Args:
            - plain_password: the plain password to be hashed.
        """
        self.pass_hash = pw_context.hash(plain_password)

    def check_password(self, plain_password: str) -> bool:
        """
        Compare the hashed password with the plain one.

        Args:
            - plain_password: the plain password to be compared with the hash.
        """
        return pw_context.verify(plain_password, self.pass_hash)

    def __repr__(self):  # pragma: no cover
        return str(self.__dict__)
