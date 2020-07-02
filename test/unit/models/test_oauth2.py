from datetime import timedelta
from unittest.mock import patch

from fastapi import HTTPException
from fastapi.params import Depends
from freezegun import freeze_time
from jwt import PyJWTError

from server.models.oauth2 import create_access_token, auth
from test.unit.factories import ApplicationFactory
from test.unit.fixtures import (
    Test,
    DEFAULT_DATETIME_STR,
    DEFAULT_DATETIME,
    TestAsync,
)


class TestCreateAccessToken(Test):
    @freeze_time(DEFAULT_DATETIME_STR)
    @patch("server.models.oauth2.env")
    @patch("server.models.oauth2.encode")
    def test_should_encode_access_token(self, encode, env):
        secret_key = self.faker.sha256()
        algorithm = self.faker.word()
        env.secret_key = secret_key
        env.token_algorithm = algorithm
        expires_at = timedelta(minutes=5)
        data = {"data_to_encode": "jubileu"}

        data_to_encode = data.copy()
        data_to_encode.update({"exp": DEFAULT_DATETIME + expires_at})

        create_access_token(data=data, expires_delta=expires_at)

        encode.assert_called_with(
            data_to_encode, secret_key, algorithm=algorithm
        )


class TestAuth(TestAsync):
    @patch("server.models.oauth2.decode")
    async def test_should_raise_auth_exception_when_decoded_token_does_not_have_sub_key(  # noqa
        self, decode
    ):
        decode.return_value = {}

        with self.assertRaises(HTTPException) as context:
            await auth()

        self.assertEqual(401, context.exception.status_code)
        self.assertEqual(
            "Could not validate your credentials.", context.exception.detail
        )

    @patch("server.models.oauth2.decode")
    async def test_should_raise_auth_exception_when_pyjwterror_is_raised(
        self, decode
    ):
        decode.side_effect = PyJWTError()

        with self.assertRaises(HTTPException) as context:
            await auth()

        self.assertEqual(401, context.exception.status_code)
        self.assertEqual(
            "Could not validate your credentials.", context.exception.detail
        )

    @patch("server.models.oauth2.decode")
    @patch("server.models.oauth2.get_app_by_uname")
    async def test_should_raise_auth_exception_when_no_app_is_found_for_the_name_provided(  # noqa
        self, get_app_by_uname, decode
    ):
        username = self.faker.user_name()
        decode.return_value = {"sub": username}
        get_app_by_uname.return_value = None

        with self.assertRaises(HTTPException) as context:
            await auth()

        self.assertEqual(401, context.exception.status_code)
        self.assertEqual(
            "Could not validate your credentials.", context.exception.detail
        )

    @patch("server.models.oauth2.decode")
    @patch("server.models.oauth2.get_app_by_uname")
    async def test_should_return_the_dependency_injection_resolver_for_db_session_when_the_app_username_is_valid(  # noqa
        self, get_app_by_uname, decode
    ):
        username = self.faker.user_name()
        decode.return_value = {"sub": username}
        get_app_by_uname.return_value = ApplicationFactory()

        self.assertIsInstance(await auth(), Depends)
