"""Added application table.

Revision ID: c08462a71a3d
Revises: 3a499648fc0a
Create Date: 2020-07-02 01:09:20.435401

"""
from alembic import op
import sqlalchemy as sa


revision = "c08462a71a3d"
down_revision = "3a499648fc0a"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "application",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("pass_hash", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index(
        op.f("ix_application_id"), "application", ["id"], unique=False
    )


def downgrade():
    op.drop_index(op.f("ix_application_id"), table_name="application")
    op.drop_table("application")
