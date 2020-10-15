from test.unit.fixtures import Test
from unittest.mock import patch

from server.db import open_session


class TestSession(Test):
    @patch("server.db.env")
    @patch("server.db.sessionmaker")
    @patch("server.db.create_engine")
    def test_should_use_correct_parameters_for_create_database_session(
        self, create_engine, sessionmaker, env
    ):
        env.DATABASE_URL = self.faker.domain_name()

        db = next(open_session())

        create_engine.assert_called_with(env.DATABASE_URL)
        sessionmaker.asset_called_with(
            bind=create_engine(), autocommit=False, autoflush=False
        )
        db.close.assert_called_once()  # noqa
