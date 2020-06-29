from unittest.mock import patch

from server.db import open_session
from test.unit.fixtures import Test


class TestSession(Test):
    @patch("server.db.env")
    @patch("server.db.sessionmaker")
    @patch("server.db.create_engine")
    def test_should_use_connect_args_when_url_contains_sqlite(
        self, create_engine, sessionmaker, env
    ):
        env.database_url = f"sqlite://{self.faker.domain_name()}"

        db = next(open_session())

        create_engine.assert_called_with(
            env.database_url, connect_args={"check_same_thread": False}
        )
        sessionmaker.asset_called_with(
            bind=create_engine(), autocommit=False, autoflush=False
        )
        db.close.assert_called_once()  # noqa

    @patch("server.db.env")
    @patch("server.db.sessionmaker")
    @patch("server.db.create_engine")
    def test_should_use_a_empty_dict_on_connect_args_when_url_has_sqlite(
        self, create_engine, sessionmaker, env
    ):
        env.database_url = self.faker.domain_name()

        db = next(open_session())

        create_engine.assert_called_with(
            env.database_url, connect_args={}
        )
        sessionmaker.asset_called_with(
            bind=create_engine(), autocommit=False, autoflush=False
        )
        db.close.assert_called_once()  # noqa
