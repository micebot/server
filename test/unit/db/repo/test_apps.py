from unittest.mock import patch, MagicMock

from server.db import entities
from server.db.repo.apps import auth_application, get_app_by_uname
from test.unit.fixtures import Test


class TestGetAppByName(Test):
    def test_should_query_using_correct_parameters(self):
        db = MagicMock()
        uname = self.faker.user_name()

        get_app_by_uname(db=db, uname=uname)

        db.query.assert_called_with(entities.Application)
        db.query().filter_by.assert_called_with(username=uname)
        db.query().filter_by().first.assert_called_once()


class TestAuthApplication(Test):
    @patch("server.db.repo.apps.get_app_by_uname", return_value=None)
    def test_should_return_none_if_no_app_is_found_for_the_username_provided(
        self, get_app_by_uname
    ):
        db = MagicMock()
        uname = self.faker.user_name()

        self.assertIsNone(
            auth_application(
                db=db, uname=uname, password=self.faker.password()
            )
        )
        get_app_by_uname.assert_called_with(db=db, uname=uname)

    @patch("server.db.repo.apps.get_app_by_uname")
    def test_should_return_none_if_the_app_password_is_incorrect(
        self, get_app_by_uname
    ):
        app = MagicMock()
        app.check_password.return_value = False
        get_app_by_uname.return_value = app

        db = MagicMock()
        uname = self.faker.user_name()
        plain_password = self.faker.password()

        self.assertIsNone(
            auth_application(db=db, uname=uname, password=plain_password)
        )
        get_app_by_uname.assert_called_with(db=db, uname=uname)
        app.check_password.assert_called_with(plain_password=plain_password)

    @patch("server.db.repo.apps.get_app_by_uname")
    def test_should_return_the_app_object_when_authenticate_successfully(
        self, get_app_by_uname
    ):
        app = MagicMock()
        app.check_password.return_value = True
        get_app_by_uname.return_value = app

        db = MagicMock()
        uname = self.faker.user_name()
        plain_password = self.faker.password()

        self.assertEqual(
            app, auth_application(db=db, uname=uname, password=plain_password)
        )
        get_app_by_uname.assert_called_with(db=db, uname=uname)
        app.check_password.assert_called_with(plain_password=plain_password)
