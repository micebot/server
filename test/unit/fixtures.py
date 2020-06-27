from typing import NoReturn
from unittest.case import TestCase
from unittest.mock import MagicMock

from faker import Faker
from fastapi.testclient import TestClient

from server import app


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
        self.app.dependency_overrides[...] = lambda: self.db

    def tearDown(self) -> NoReturn:
        self.app.dependency_overrides = {}
