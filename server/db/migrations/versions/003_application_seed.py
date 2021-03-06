"""Applications seed.

Revision ID: 349f8f05fa5e
Revises: c08462a71a3d
Create Date: 2020-07-02 01:10:46.950587

"""
from os import environ

import sqlalchemy as sa
from alembic import op

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
    """Added the initial applications user/pass."""
    ps_app = Application(
        username=environ.get("PUBSUB_USER") if env.PRODUCTION else "ps_user"
    )
    ps_app.password = (
        environ.get("PUBSUB_PASS") if env.PRODUCTION else "ps_pass"
    )

    ds_app = Application(
        username=environ.get("DISCORD_USER") if env.PRODUCTION else "ds_user"
    )
    ds_app.password = (
        environ.get("DISCORD_PASS") if env.PRODUCTION else "ds_pass"
    )

    op.bulk_insert(
        t_app,
        [
            {"username": app.username, "pass_hash": app.password}
            for app in [ps_app, ds_app]
        ],
    )


def downgrade():
    """Remove all registers from application table."""
    op.execute(t_app.delete())
