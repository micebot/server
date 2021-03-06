from test.unit.factories import OrderFactory, ProductFactory
from test.unit.fixtures import TestHelpers, TestRoute
from typing import NoReturn
from unittest.mock import patch


class TestGetAllOrders(TestRoute):
    def setUp(self) -> NoReturn:
        super().setUp()
        self.skip = self.faker.pyint()
        self.limit = self.faker.pyint()
        self.moderator = self.faker.user_name()
        self.owner = self.faker.user_name()
        self.desc = self.faker.boolean()

    @patch("server.routes.orders.repo.get_orders_count")
    @patch("server.routes.orders.repo.get_orders")
    def test_should_return_200_with_entities(
        self, get_orders, get_orders_count
    ):
        order = OrderFactory()

        orders_list = [order]
        orders_count = len(orders_list)

        get_orders.return_value = orders_list
        get_orders_count.return_value = orders_count

        response = self.client.get(
            "/orders",
            params={
                "skip": self.skip,
                "limit": self.limit,
                "moderator": self.moderator,
                "owner": self.owner,
                "desc": self.desc,
            },
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {
                "total": orders_count,
                "orders": [
                    {
                        "uuid": order.uuid,
                        "mod_id": order.mod_id,
                        "mod_display_name": order.mod_display_name,
                        "owner_display_name": order.owner_display_name,
                        "requested_at": TestHelpers.datetime_to_str(
                            order.requested_at
                        ),
                        "product": {
                            "code": order.product.code,
                            "summary": order.product.summary,
                            "uuid": order.product.uuid,
                            "taken": order.product.taken,
                            "created_at": TestHelpers.datetime_to_str(
                                order.product.created_at
                            ),
                            "updated_at": TestHelpers.datetime_to_str(
                                order.product.updated_at
                            ),
                        },
                    }
                ],
            },
            response.json(),
        )

        get_orders_count.assert_called_with(db=self.db)
        get_orders.assert_called_with(
            db=self.db,
            skip=self.skip,
            limit=self.limit,
            moderator=self.moderator,
            owner=self.owner,
            desc=self.desc,
        )


class TestPost(TestRoute):
    def setUp(self) -> NoReturn:
        super().setUp()
        self.uuid = self.faker.uuid4()
        self.payload = {
            "mod_id": self.faker.md5(),
            "mod_display_name": self.faker.user_name(),
            "owner_display_name": self.faker.user_name(),
        }

    @patch("server.routes.orders.product_repo.get_product_by_uuid")
    def test_should_return_404_when_the_product_uuid_is_not_found(
        self, get_product_by_uuid
    ):
        get_product_by_uuid.return_value = None

        response = self.client.post(f"/orders/{self.uuid}", json=self.payload)

        self.assertEqual(404, response.status_code)
        self.assertEqual(
            {"detail": "No product found for the uuid provided."},
            response.json(),
        )
        get_product_by_uuid.assert_called_with(db=self.db, uuid=self.uuid)

    @patch("server.routes.orders.product_repo.get_product_by_uuid")
    def test_should_return_409_when_the_product_uuid_already_taken(
        self, get_product_by_uuid
    ):
        get_product_by_uuid.return_value = ProductFactory(taken=True)

        response = self.client.post(f"/orders/{self.uuid}", json=self.payload)

        self.assertEqual(409, response.status_code)
        self.assertEqual(
            {"detail": "The product code is already taken."},
            response.json(),
        )
        get_product_by_uuid.assert_called_with(db=self.db, uuid=self.uuid)

    @patch("server.routes.orders.repo.create_order_for_product")
    @patch("server.routes.orders.product_repo.get_product_by_uuid")
    def test_should_return_200_and_create_a_new_order(
        self, get_product_by_uuid, create_order_for_product
    ):
        product = ProductFactory(taken=False)
        order = OrderFactory(product__taken=True)

        get_product_by_uuid.return_value = product
        create_order_for_product.return_value = order

        response = self.client.post(f"/orders/{self.uuid}", json=self.payload)

        self.assertEqual(201, response.status_code)

        self.assertEqual(
            {
                "mod_id": order.mod_id,
                "mod_display_name": order.mod_display_name,
                "owner_display_name": order.owner_display_name,
                "uuid": order.uuid,
                "requested_at": TestHelpers.datetime_to_str(
                    order.requested_at
                ),
                "product": {
                    "code": order.product.code,
                    "summary": order.product.summary,
                    "uuid": order.product.uuid,
                    "taken": order.product.taken,
                    "created_at": TestHelpers.datetime_to_str(
                        order.product.created_at
                    ),
                    "updated_at": TestHelpers.datetime_to_str(
                        order.product.updated_at
                    ),
                },
            },
            response.json(),
        )

        get_product_by_uuid.assert_called_with(db=self.db, uuid=self.uuid)
