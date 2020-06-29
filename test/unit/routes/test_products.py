from typing import NoReturn
from unittest.mock import patch

from server.models import schemas
from test.unit.factories import ProductFactory
from test.unit.fixtures import TestRoute, TestHelpers


class TestGet(TestRoute):
    def setUp(self) -> NoReturn:
        super().setUp()
        self.skip = self.faker.pyint()
        self.limit = self.faker.pyint()
        self.taken = self.faker.boolean()

    @patch("server.routes.products.repo.get_products")
    def test_should_return_404_when_there_are_no_products_registered(
        self, get_products
    ):
        get_products.return_value = None

        response = self.client.get(
            "/products",
            params={
                "skip": self.skip,
                "limit": self.limit,
                "taken": self.taken,
            },
        )
        self.assertEqual(404, response.status_code)
        self.assertEqual(
            {"detail": "No products registered yet."}, response.json()
        )

        get_products.assert_called_with(
            db=self.db, skip=self.skip, limit=self.limit, taken=self.taken
        )

    @patch("server.routes.products.repo.get_products")
    def test_should_return_200_with_entities(self, get_products):
        product = ProductFactory()
        get_products.return_value = [product]

        response = self.client.get(
            "/products",
            params={
                "skip": self.skip,
                "limit": self.limit,
                "taken": self.taken,
            },
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(
            [
                {
                    "code": product.code,
                    "summary": product.summary,
                    "id": product.id,
                    "taken": product.taken,
                    "taken_at": TestHelpers.datetime_to_str(product.taken_at),
                }
            ],
            response.json(),
        )

        get_products.assert_called_with(
            db=self.db, skip=self.skip, limit=self.limit, taken=self.taken
        )


class TestPost(TestRoute):
    @patch("server.routes.products.repo.create_product")
    @patch("server.routes.products.repo.get_product_by_code")
    def test_should_return_409_when_the_code_is_already_registed(
        self, get_product_by_code, create_product
    ):
        product = ProductFactory()
        get_product_by_code.return_value = product

        response = self.client.post(
            "/products/",
            json={"code": product.code, "summary": product.summary},
        )

        self.assertEqual(409, response.status_code)
        self.assertEqual(
            {"detail": "The code is already in use by another product."},
            response.json(),
        )

        get_product_by_code.assert_called_with(db=self.db, code=product.code)
        create_product.assert_not_called()

    @patch("server.routes.products.repo.create_product")
    @patch("server.routes.products.repo.get_product_by_code")
    def test_should_return_201_when_the_product_is_registered_successfully(
        self, get_product_by_code, create_product
    ):
        product = ProductFactory()
        get_product_by_code.return_value = None
        create_product.return_value = product

        response = self.client.post(
            "/products/",
            json={"code": product.code, "summary": product.summary},
        )

        self.assertEqual(201, response.status_code)
        self.assertEqual(
            {
                "code": product.code,
                "summary": product.summary,
                "id": product.id,
                "taken": product.taken,
                "taken_at": TestHelpers.datetime_to_str(product.taken_at),
            },
            response.json(),
        )
        get_product_by_code.assert_called_with(db=self.db, code=product.code)


class TestPut(TestRoute):
    def setUp(self) -> NoReturn:
        super().setUp()
        self.product = ProductFactory()

    @patch("server.routes.products.repo.update_product")
    @patch("server.routes.products.repo.get_product_by_code")
    def test_should_return_404_when_no_product_are_found_for_the_code_provided(
        self, get_product_by_code, update_product
    ):
        code_to_update = self.faker.md5()
        get_product_by_code.return_value = None

        response = self.client.put(
            f"/products/{code_to_update}",
            json={"code": self.product.code, "summary": self.product.summary},
        )

        self.assertEqual(404, response.status_code)
        self.assertEqual(
            {"detail": "No product found for the code specified."},
            response.json(),
        )
        get_product_by_code.assert_called_with(db=self.db, code=code_to_update)
        update_product.assert_not_called()

    @patch("server.routes.products.repo.update_product")
    @patch("server.routes.products.repo.get_product_by_code")
    def test_should_return_409_when_the_new_code_is_already_in_use_by_another_project(  # noqa
        self, get_product_by_code, update_product
    ):
        code_to_update = self.faker.md5()
        product_to_update = ProductFactory()
        product_with_code_already_in_use = ProductFactory()

        get_product_by_code.side_effect = [
            product_to_update,
            product_with_code_already_in_use,
        ]

        response = self.client.put(
            f"/products/{code_to_update}",
            json={"code": self.product.code, "summary": self.product.summary},
        )

        self.assertEqual(409, response.status_code)
        self.assertEqual(
            {"detail": "The code is already in use by another product."},
            response.json(),
        )
        get_product_by_code.assert_any_call(db=self.db, code=code_to_update)
        get_product_by_code.assert_any_call(db=self.db, code=self.product.code)
        self.assertEqual(2, get_product_by_code.call_count)
        update_product.assert_not_called()

    @patch("server.routes.products.repo.update_product")
    @patch("server.routes.products.repo.get_product_by_code")
    def test_should_return_200_with_the_updated_product(
        self, get_product_by_code, update_product
    ):
        code_to_update = self.faker.md5()
        product_to_update = ProductFactory()
        updated_product = ProductFactory(
            code=self.product.code, summary=self.product.summary
        )

        get_product_by_code.side_effect = [
            product_to_update,
            None,
        ]
        update_product.return_value = updated_product

        response = self.client.put(
            f"/products/{code_to_update}",
            json={"code": self.product.code, "summary": self.product.summary},
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {
                "code": updated_product.code,
                "summary": updated_product.summary,
                "id": updated_product.id,
                "taken": updated_product.taken,
                "taken_at": TestHelpers.datetime_to_str(
                    updated_product.taken_at
                ),
            },
            response.json(),
        )

        get_product_by_code.assert_any_call(db=self.db, code=code_to_update)
        get_product_by_code.assert_any_call(db=self.db, code=self.product.code)
        self.assertEqual(2, get_product_by_code.call_count)
        update_product.assert_called_with(
            db=self.db,
            product=schemas.ProductUpdate(
                code=self.product.code, summary=self.product.summary
            ),
            db_product=product_to_update,
        )


class TestDelete(TestRoute):
    def setUp(self) -> NoReturn:
        super().setUp()
        self.code_to_delete = self.faker.md5()

    @patch("server.routes.products.repo.delete_product")
    @patch("server.routes.products.repo.get_product_by_code")
    def test_should_return_404_when_no_product_are_found_for_the_code_provided(
        self, get_product_by_code, delete_product
    ):
        get_product_by_code.return_value = None

        response = self.client.delete(f"/products/{self.code_to_delete}")

        self.assertEqual(404, response.status_code)
        self.assertEqual(
            {"detail": "No product found for the code specified."},
            response.json(),
        )
        get_product_by_code.assert_called_with(
            db=self.db, code=self.code_to_delete
        )
        delete_product.assert_not_called()

    @patch("server.routes.products.repo.delete_product")
    @patch("server.routes.products.repo.get_product_by_code")
    def test_should_return_401_when_the_product_is_already_taken(
        self, get_product_by_code, delete_product
    ):
        get_product_by_code.return_value = ProductFactory(taken=True)

        response = self.client.delete(f"/products/{self.code_to_delete}")

        self.assertEqual(401, response.status_code)
        self.assertEqual(
            {"detail": "Cannot delete products already taken."},
            response.json(),
        )
        get_product_by_code.assert_called_with(
            db=self.db, code=self.code_to_delete
        )
        delete_product.assert_not_called()

    @patch("server.routes.products.repo.delete_product")
    @patch("server.routes.products.repo.get_product_by_code")
    def test_should_return_200_and_remove_the_product(
        self, get_product_by_code, delete_product
    ):
        product = ProductFactory(taken=False)
        get_product_by_code.return_value = product

        response = self.client.delete(f"/products/{self.code_to_delete}")

        self.assertEqual(200, response.status_code)
        self.assertEqual({"deleted": True}, response.json())

        get_product_by_code.assert_called_with(
            db=self.db, code=self.code_to_delete
        )
        delete_product.assert_called_with(db=self.db, product=product)
