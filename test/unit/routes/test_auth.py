from unittest.mock import patch

from test.unit.factories import ApplicationFactory
from test.unit.fixtures import TestRoute


class TestPost(TestRoute):
    @patch("server.routes.auth.auth_application", return_value=None)
    def test_should_return_401_when_the_authencation_fails(
        self, auth_application
    ):

        username = self.faker.user_name()
        password = self.faker.password()

        response = self.client.post(
            "/auth/", data={"username": username, "password": password}
        )

        self.assertTrue(
            ("WWW-authenticate", "Bearer") in response.headers.items()
        )
        self.assertEqual(401, response.status_code)
        self.assertEqual(
            {"detail": "Invalid or unknown client application."},
            response.json(),
        )
        auth_application.assert_called_with(
            db=self.db, uname=username, password=password
        )

    @patch("server.routes.auth.auth_application")
    @patch("server.routes.auth.create_access_token")
    def test_should_create_the_access_token_when_authenticate_successfully(
        self, create_access_token, auth_application
    ):
        app = ApplicationFactory()
        access_token = self.faker.sha256()

        auth_application.return_value = app
        create_access_token.return_value = access_token

        username = self.faker.user_name()
        password = self.faker.password()

        response = self.client.post(
            "/auth/", data={"username": username, "password": password}
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual({
            'access_token': access_token,
            'token_type': 'bearer'
        }, response.json())

        auth_application.assert_called_with(
            db=self.db, uname=username, password=password
        )
        create_access_token.assert_called_with(data={"sub": app.username})
