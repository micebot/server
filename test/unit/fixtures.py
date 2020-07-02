from datetime import datetime
from typing import NoReturn, Optional
from unittest.async_case import IsolatedAsyncioTestCase
from unittest.case import TestCase
from unittest.mock import MagicMock

from faker import Faker
from fastapi.testclient import TestClient

from server import app
from server.db import open_session
from server.models.oauth2 import auth, oauth_schema


class Test(TestCase):
    @classmethod
    def setUpClass(cls) -> NoReturn:
        cls.faker = Faker(locale="pt_BR")


class TestRoute(Test):
    @classmethod
    def setUpClass(cls) -> NoReturn:
        super().setUpClass()
        cls.client = TestClient(app=app)
        cls.app = app

    def setUp(self) -> NoReturn:
        self.db = MagicMock()
        self.app.dependency_overrides[oauth_schema] = lambda: "token"
        self.app.dependency_overrides[open_session] = lambda: self.db
        self.app.dependency_overrides[auth] = lambda: self.db

    def tearDown(self) -> NoReturn:
        self.app.dependency_overrides = {}


class TestAsync(IsolatedAsyncioTestCase, Test):
    """Use it for test 'async' functions."""


class TestHelpers:
    @staticmethod
    def datetime_to_str(dt: datetime) -> Optional[str]:
        if not dt:
            return None
        return dt.strftime("%Y-%m-%dT%H:%M:%S")


DEFAULT_DATETIME_STR = "2020-06-30 00:00:00"
DEFAULT_DATETIME = datetime(2020, 6, 30, 00, 00, 00)
