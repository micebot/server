"""Added uuid to products and orders.

Revision ID: acac5d708491
Revises: 349f8f05fa5e
Create Date: 2020-07-03 12:56:43.725996

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "acac5d708491"
down_revision = "349f8f05fa5e"
branch_labels = None
depends_on = None


def upgrade():
    """Added uuid for tables 'order' and 'product'."""
    op.add_column(
        "order",
        sa.Column("uuid", postgresql.UUID(as_uuid=True), nullable=False),
    )
    op.create_unique_constraint("uq_uuid_order", "order", ["uuid"])
    op.add_column(
        "product",
        sa.Column("uuid", postgresql.UUID(as_uuid=True), nullable=False),
    )
    op.create_unique_constraint("uq_uuid_product", "product", ["uuid"])


def downgrade():
    """Remove the uuid column from 'order' and 'product' tables."""
    op.drop_constraint("uq_uuid_product", "product")
    op.drop_column("product", "uuid")
    op.drop_constraint("uq_uuid_order", "order")
    op.drop_column("order", "uuid")
