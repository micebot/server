from unittest.mock import MagicMock, patch

from server.db import entities
from server.db.repo.orders import (
    get_orders,
    get_order_by_product_code,
    create_order_for_product,
    get_orders_count,
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

    @patch("server.db.repo.orders.entities.Order")
    def test_should_query_using_default_parameters_on_get_orders(
        self, order_instance
    ):
        asc_request_at = MagicMock()
        desc_request_at = MagicMock()

        order_instance.requested_at.desc.return_value = desc_request_at
        order_instance.requested_at.asc.return_value = asc_request_at

        db = MagicMock()
        db_query = MagicMock()
        db.query.return_value = db_query

        get_orders(db=db)

        db.query.assert_called_with(entities.Order)
        db.query().order_by.assert_called_with(desc_request_at)
        db_query.order_by().offset.assert_called_with(0)
        db_query.order_by().offset().limit.assert_called_with(50)
        db_query.order_by().offset().limit().all.assert_called_once()

        order_instance.requested_at.asc.assert_not_called()
        order_instance.requested_at.desc.assert_called_once()

    @patch("server.db.repo.orders.entities.Order")
    def test_should_query_using_correct_parameters_on_get_orders(
        self, order_instance
    ):
        asc_request_at = MagicMock()
        desc_request_at = MagicMock()

        order_instance.requested_at.desc.return_value = desc_request_at
        order_instance.requested_at.asc.return_value = asc_request_at

        db = MagicMock()
        db_query = MagicMock()
        db.query.return_value = db_query

        skip = self.faker.pyint()
        limit = self.faker.pyint()

        get_orders(db=db, skip=skip, limit=limit, desc=False)

        db.query.assert_called_with(entities.Order)
        db.query().order_by.assert_called_with(asc_request_at)
        db_query.order_by().offset.assert_called_with(skip)
        db_query.order_by().offset().limit.assert_called_with(limit)
        db_query.order_by().offset().limit().all.assert_called_once()

        order_instance.requested_at.asc.assert_called_once()
        order_instance.requested_at.desc.assert_not_called()


class TestGetOrdersCount(Test):
    def test_should_count_the_orders_entities(self):
        db = MagicMock()

        get_orders_count(db=db)

        db.query.assert_called_with(entities.Order)
        db.query().count.assert_called_once()


class TestGetOrderByProductCode(Test):
    def test_should_query_using_correct_parameters(self):
        db = MagicMock()
        code = self.faker.sha256()

        get_order_by_product_code(db=db, code=code)

        db.query.assert_called_with(entities.Order)
        db.query().join.assert_called_with(entities.Product)
        db.query().join().filter.assert_called_once()
        db.query().join().filter().first.assert_called_once()


class TestCreateOrderForProduct(Test):
    @patch("server.db.repo.orders.entities.Order")
    def test_should_persist_and_mark_product_as_taken(self, order_instance):
        db = MagicMock()
        db_order = OrderFactory(product__taken=False)
        order_instance.return_value = db_order

        order = schemas.OrderCreation(
            mod_id=db_order.mod_id,
            mod_display_name=db_order.mod_display_name,
            owner_display_name=db_order.owner_display_name,
        )

        db_order = create_order_for_product(
            db=db, product=db_order.product, order=order
        )
        self.assertTrue(db_order.product.taken)

        db.add.assert_called_with(db_order)
        db.commit.assert_called_once()
        db.refresh.assert_called_with(db_order)
