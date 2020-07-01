from datetime import datetime
from unittest.mock import MagicMock, patch

from freezegun import freeze_time

from server.db import entities
from server.db.repo.orders import (
    get_order_by_id,
    get_order_by_product_id,
    create_order,
    take_order,
    get_orders,
)
from server.models import schemas
from test.unit.factories import OrderFactory
from test.unit.fixtures import Test


class TestGetOrders(Test):
    def test_should_apply_moderator_display_name_filter_when_specified(self):
        db = MagicMock()
        mod_display_name = self.faker.user_name()

        get_orders(db=db, moderator=mod_display_name)

        db.query.assert_called_with(entities.Order)
        db.query.filter_by(mod_display_name=mod_display_name)

    def test_should_apply_owner_display_name_filter_when_specified(self):
        db = MagicMock()
        owner_display_name = self.faker.user_name()

        get_orders(db=db, owner=owner_display_name)

        db.query.assert_called_with(entities.Order)
        db.query.filter_by(owner_display_name=owner_display_name)

    def test_should_query_using_default_parameters(self):
        db = MagicMock()
        db_query = MagicMock()
        db.query.return_value = db_query

        get_orders(db=db)

        db.query.assert_called_with(entities.Order)
        db_query.filter.assert_called_once()
        db_query.filter().offset.assert_called_with(0)
        db_query.filter().offset().limit.assert_called_with(50)
        db_query.filter().offset().limit().all.assert_called_once()

    def test_should_query_using_correct_parameters(self):
        db = MagicMock()
        db_query = MagicMock()
        db.query.return_value = db_query

        skip = self.faker.pyint()
        limit = self.faker.pyint()

        get_orders(
            db=db,
            skip=skip,
            limit=limit,
        )

        db.query.assert_called_with(entities.Order)
        db_query.filter.assert_called_once()
        db_query.filter().offset.assert_called_with(skip)
        db_query.filter().offset().limit.assert_called_with(limit)
        db_query.filter().offset().limit().all.assert_called_once()


class TestGetOrderById(Test):
    def test_should_query_using_correct_parameters(self):
        db = MagicMock()
        order_id = self.faker.pyint()

        get_order_by_id(db=db, order_id=order_id)

        db.query.assert_called_with(entities.Order)
        db.query().filter_by(id=order_id)
        db.query().filter_by().first.assert_called_once()


class TestGetOrderByProductId(Test):
    def test_should_add_order_commit_and_refresh_object(self):
        db = MagicMock()
        product_id = self.faker.pyint()

        get_order_by_product_id(db=db, product_id=product_id)

        db.query.assert_called_with(entities.Order)
        db.query().filter_by(product_id=product_id)
        db.query().filter_by().first.assert_called_once()


class TestCreateOrder(Test):
    @patch("server.db.repo.orders.entities.Order")
    def test_should_query_using_correct_parameters(self, order_instance):
        db = MagicMock()

        order = schemas.OrderCreation(
            mod_id=self.faker.md5(),
            mod_display_name=self.faker.user_name(),
            owner_display_name=self.faker.user_name(),
            product_id=self.faker.pyint(),
        )
        db_order = OrderFactory(
            mod_id=order.mod_id,
            mod_display_name=order.mod_display_name,
            owner_display_name=order.owner_display_name,
            product_id=order.product_id,
        )

        order_instance.return_value = db_order

        create_order(db=db, order=order)

        db.add.assert_called_with(db_order)
        db.commit.assert_called_once()
        db.refresh.assert_called_with(db_order)


class TestTakeOrder(Test):
    @freeze_time("2020-06-30 00:00:00")
    def test_should_change_the_product_taken_to_true_and_commit(self):
        db = MagicMock()
        order = OrderFactory(product__taken=False, product__taken_at=None)

        db_updated = take_order(db=db, order=order)

        self.assertTrue(db_updated.product.taken)
        self.assertEqual(
            datetime(2020, 6, 30, 00, 00, 00), db_updated.product.taken_at
        )
        db.commit.assert_called_once()
