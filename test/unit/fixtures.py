from datetime import datetime
from typing import NoReturn, Optional
from unittest.case import TestCase
from unittest.mock import MagicMock

from faker import Faker
from fastapi.testclient import TestClient

from server import app
from server.models.oauth2 import auth


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
        self.app.dependency_overrides[auth] = lambda: self.db

    def tearDown(self) -> NoReturn:
        self.app.dependency_overrides = {}


class TestHelpers:
    @staticmethod
    def datetime_to_str(dt: datetime) -> Optional[str]:
        if not dt:
            return None
        return dt.strftime("%Y-%m-%dT%H:%M:%S")
