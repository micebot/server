"""Initial database schema.

Revision ID: 3a499648fc0a
Revises:
Create Date: 2020-06-28 00:19:00.172558

"""
import sqlalchemy as sa
from alembic import op

revision = "3a499648fc0a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Create the initial database schema."""
    op.create_table(
        "product",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(), nullable=False),
        sa.Column("summary", sa.String(), nullable=False),
        sa.Column("taken", sa.Boolean(), nullable=False),
        sa.Column("taken_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_product_code"), "product", ["code"], unique=True)
    op.create_index(op.f("ix_product_id"), "product", ["id"], unique=False)
    op.create_table(
        "order",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("mod_id", sa.String(), nullable=False),
        sa.Column("mod_display_name", sa.String(), nullable=False),
        sa.Column("owner_display_name", sa.String(), nullable=False),
        sa.Column("requested_at", sa.DateTime(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["product_id"], ["product.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_order_id"), "order", ["id"], unique=False)


def downgrade():
    """Drop all tables and indexes from database."""
    op.drop_index(op.f("ix_order_id"), table_name="order")
    op.drop_table("order")
    op.drop_index(op.f("ix_product_id"), table_name="product")
    op.drop_index(op.f("ix_product_code"), table_name="product")
    op.drop_table("product")
