from typing import NoReturn
from unittest.mock import patch

from test.unit.factories import OrderFactory
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
