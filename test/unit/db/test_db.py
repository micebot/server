from test.unit.fixtures import Test
from unittest.mock import patch

from server.db import open_session


class TestSession(Test):
    @patch("server.db.SessionLocal")
    def test_should_use_correct_parameters_for_create_database_session(
        self,
        session_local,
    ):
        db = next(open_session())
        db.close.assert_called_once()
