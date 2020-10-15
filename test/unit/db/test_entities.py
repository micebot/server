from test.unit.factories import ApplicationFactory
from test.unit.fixtures import Test
from unittest.mock import patch


class TestApplication(Test):
    @patch("server.db.entities.pw_context.hash")
    def test_should_hash_password_when_use_setter_from_password_property(
        self, hash
    ):
        app = ApplicationFactory()
        plain_password = self.faker.password()

        app.password = plain_password

        hash.assert_called_with(plain_password)

    def test_should_get_hash_password_when_use_getter_from_password_property(
        self,
    ):
        app = ApplicationFactory()
        self.assertEqual(app.pass_hash, app.password)

    @patch("server.db.entities.pw_context.verify", return_value=False)
    def test_should_verify_hash_when_call_check_password(self, verifiy):
        app = ApplicationFactory()
        plain_password = self.faker.password()

        self.assertFalse(app.check_password(plain_password))
        verifiy.assert_called_with(plain_password, app.pass_hash)
