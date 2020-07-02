"""Applications seed.

Revision ID: 349f8f05fa5e
Revises: c08462a71a3d
Create Date: 2020-07-02 01:10:46.950587

"""
from os import environ

from alembic import op
import sqlalchemy as sa

from server import env
from server.db.entities import Application

revision = "349f8f05fa5e"
down_revision = "c08462a71a3d"
branch_labels = None
depends_on = None

t_app = sa.table(
    "application",
    sa.column("id", sa.Integer),
    sa.column("username", sa.String),
    sa.column("pass_hash", sa.String),
)


def upgrade():
    ps_app = Application(
        username=environ.get("PS_USER") if env.production else "ps_user"
    )
    ps_app.password = environ.get("PS_PASS") if env.production else "ps_pass"

    ds_app = Application(
        username=environ.get("DS_USER") if env.production else "ds_user"
    )
    ds_app.password = environ.get("DS_PASS") if env.production else "ds_pass"

    op.bulk_insert(
        t_app,
        [
            {"username": app.username, "pass_hash": app.password}
            for app in [ps_app, ds_app]
        ],
    )


def downgrade():
    op.execute(t_app.delete())
