"""Added created_at and updated_at to product.

Revision ID: 1ba1b384f25c
Revises: acac5d708491
Create Date: 2020-07-20 17:20:32.954964

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "1ba1b384f25c"
down_revision = "acac5d708491"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "product",
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.add_column(
        "product",
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.drop_column("product", "taken_at")


def downgrade():
    op.add_column(
        "product",
        sa.Column(
            "taken_at",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.drop_column("product", "updated_at")
    op.drop_column("product", "created_at")
