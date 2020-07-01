from typing import NoReturn, Dict, Any
from unittest.mock import patch

from server.models import schemas
from test.unit.factories import OrderFactory, ProductFactory
from test.unit.fixtures import TestRoute, TestHelpers


class TestGet(TestRoute):
    def setUp(self) -> NoReturn:
        super().setUp()
        self.skip = self.faker.pyint()
        self.limit = self.faker.pyint()
        self.taken = self.faker.boolean()
        self.moderator = self.faker.user_name()
        self.owner = self.faker.user_name()

    @patch("server.routes.orders.repo.get_orders")
    def test_should_return_404_when_there_are_no_orders_registered(
        self, get_orders
    ):
        get_orders.return_value = None

        response = self.client.get(
            "/orders",
            params={
                "skip": self.skip,
                "limit": self.limit,
                "moderator": self.moderator,
                "owner": self.owner,
                "taken": self.taken,
            },
        )
        self.assertEqual(404, response.status_code)
        self.assertEqual(
            {"detail": "No orders registered yet."}, response.json()
        )

        get_orders.assert_called_with(
            db=self.db,
            skip=self.skip,
            limit=self.limit,
            moderator=self.moderator,
            owner=self.owner,
            taken=self.taken,
        )

    @patch("server.routes.orders.repo.get_orders")
    def test_should_return_200_with_entities(self, get_orders):
        order = OrderFactory()
        get_orders.return_value = [order]

        response = self.client.get(
            "/orders",
            params={
                "skip": self.skip,
                "limit": self.limit,
                "moderator": self.moderator,
                "owner": self.owner,
                "taken": self.taken,
            },
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(
            [
                {
                    "id": order.id,
                    "mod_id": order.mod_id,
                    "mod_display_name": order.mod_display_name,
                    "owner_display_name": order.owner_display_name,
                    "requested_at": TestHelpers.datetime_to_str(
                        order.requested_at
                    ),
                    "product": {
                        "code": order.product.code,
                        "summary": order.product.summary,
                        "id": order.product.id,
                        "taken": order.product.taken,
                        "taken_at": TestHelpers.datetime_to_str(
                            order.product.taken_at
                        ),
                    },
                }
            ],
            response.json(),
        )

        get_orders.assert_called_with(
            db=self.db,
            skip=self.skip,
            limit=self.limit,
            moderator=self.moderator,
            owner=self.owner,
            taken=self.taken,
        )


class TestPost(TestRoute):
    def setUp(self) -> NoReturn:
        super().setUp()
        self.payload = {
            "mod_id": self.faker.md5(),
            "mod_display_name": self.faker.user_name(),
            "owner_display_name": self.faker.user_name(),
            "product_id": self.faker.pyint(),
        }

    @patch("server.routes.orders.repo.get_order_by_product_id")
    def test_should_return_409_when_product_id_is_already_registed_for_other_order(  # noqa
        self, get_order_by_product_id
    ):
        get_order_by_product_id.return_value = OrderFactory(
            product__id=self.payload.get("product_id")
        )

        response = self.client.post("/orders/", json=self.payload)

        self.assertEqual(409, response.status_code)
        self.assertEqual(
            {"detail": "The product id is already in use by another order."},
            response.json(),
        )

        get_order_by_product_id.assert_called_with(
            db=self.db, product_id=self.payload.get("product_id")
        )

    @patch("server.routes.orders.repo.create_order")
    @patch("server.routes.orders.repo.get_order_by_product_id")
    def test_should_create_a_new_orders(
        self, get_order_by_product_id, create_order
    ):
        get_order_by_product_id.return_value = None

        product = ProductFactory()
        order = OrderFactory(
            mod_id=self.payload.get("mod_id"),
            mod_display_name=self.payload.get("mod_display_name"),
            owner_display_name=self.payload.get("owner_display_name"),
            product=product,
            product_id=product.id,
        )
        get_order_by_product_id.return_value = None
        create_order.return_value = order

        response = self.client.post("/orders/", json=self.payload)

        self.assertEqual(201, response.status_code)
        self.assertEqual(
            {
                "mod_id": order.mod_id,
                "mod_display_name": order.mod_display_name,
                "owner_display_name": order.owner_display_name,
                "id": order.id,
                "requested_at": TestHelpers.datetime_to_str(
                    order.requested_at
                ),
                "product": {
                    "code": order.product.code,
                    "summary": order.product.summary,
                    "id": order.product.id,
                    "taken": order.product.taken,
                    "taken_at": TestHelpers.datetime_to_str(
                        order.product.taken_at
                    ),
                },
            },
            response.json(),
        )

        get_order_by_product_id.assert_called_with(
            db=self.db, product_id=self.payload.get("product_id")
        )
        create_order.assert_called_with(
            db=self.db,
            order=schemas.OrderCreation(
                mod_id=self.payload.get("mod_id"),
                mod_display_name=self.payload.get("mod_display_name"),
                owner_display_name=self.payload.get("owner_display_name"),
                product_id=self.payload.get("product_id"),
            ),
        )


class TestPutTake(TestRoute):
    @patch("server.routes.orders.repo.get_order_by_id")
    def test_should_return_404_when_no_order_exists_for_id_provided(
        self, get_order_by_id
    ):
        get_order_by_id.return_value = None
        order_id = self.faker.pyint()

        response = self.client.put(f"/orders/take/{order_id}")
        self.assertEqual(404, response.status_code)
        self.assertEqual(
            {"detail": "No order found for the id specified."}, response.json()
        )

    @patch("server.routes.orders.repo.get_order_by_id")
    def test_should_return_409_when_the_order_is_already_taken(
            self, get_order_by_id
    ):
        order = OrderFactory(product__taken=True)
        get_order_by_id.return_value = order

        response = self.client.put(f"/orders/take/{order.id}")
        self.assertEqual(409, response.status_code)
        self.assertEqual(
            {"detail": "The product for this order is already taken."},
            response.json(),
        )

    @patch("server.routes.orders.repo.take_order")
    @patch("server.routes.orders.repo.get_order_by_id")
    def test_should_return_200_when_changes_the_product_order_as_taken(
            self, get_order_by_id, take_order
    ):
        order = OrderFactory(product__taken=False)
        taken_order = OrderFactory(product__taken=True)

        get_order_by_id.return_value = order
        take_order.return_value = taken_order

        response = self.client.put(f"/orders/take/{order.id}")
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {
                "mod_id": taken_order.mod_id,
                "mod_display_name": taken_order.mod_display_name,
                "owner_display_name": taken_order.owner_display_name,
                "id": taken_order.id,
                "requested_at": TestHelpers.datetime_to_str(
                    taken_order.requested_at
                ),
                "product": {
                    "code": taken_order.product.code,
                    "summary": taken_order.product.summary,
                    "id": taken_order.product.id,
                    "taken": taken_order.product.taken,
                    "taken_at": TestHelpers.datetime_to_str(
                        taken_order.product.taken_at
                    ),
                },
            },
            response.json(),
        )
