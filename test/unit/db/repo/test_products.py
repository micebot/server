from unittest.mock import MagicMock, patch

from server.db import entities
from server.db.repo.products import (
    get_products,
    create_product,
    update_product,
    delete_product,
    get_product_by_uuid,
    get_product_by_code,
)
from server.models import schemas
from test.unit.factories import ProductFactory
from test.unit.fixtures import Test


class TestGetProducts(Test):
    def test_should_query_using_default_parameters(self):
        db = MagicMock()

        get_products(db=db)

        db.query.assert_called_with(entities.Product)
        db.query().filter_by.assert_called_with(taken=False)
        db.query().filter_by().offset.assert_called_with(0)
        db.query().filter_by().offset().limit.assert_called_with(50)
        db.query().filter_by().offset().limit().all.assert_called_once()

    def test_should_query_using_the_specified_parameters(self):

        skip = self.faker.pyint()
        limit = self.faker.pyint()
        taken = self.faker.boolean()

        db = MagicMock()

        get_products(db=db, skip=skip, limit=limit, taken=taken)

        db.query.assert_called_with(entities.Product)
        db.query().filter_by.assert_called_with(taken=taken)
        db.query().filter_by().offset.assert_called_with(skip)
        db.query().filter_by().offset().limit.assert_called_with(limit)
        db.query().filter_by().offset().limit().all.assert_called_once()


class TestGetProductByUUID(Test):
    def test_should_execute_query_with_specified_parameters(self):
        db = MagicMock()
        uuid = self.faker.uuid4()

        get_product_by_uuid(db=db, uuid=uuid)

        db.query.assert_called_with(entities.Product)
        db.query().filter_by.assert_called_with(uuid=uuid)
        db.query().filter_by().first.assert_called_once()


class TestGetProductByCode(Test):
    def test_should_execute_query_with_specified_parameters(self):
        db = MagicMock()
        code = self.faker.word()

        get_product_by_code(db=db, code=code)

        db.query.assert_called_with(entities.Product)
        db.query().filter_by.assert_called_with(code=code)
        db.query().filter_by().first.assert_called_once()


class TestCreateProduct(Test):
    @patch("server.db.repo.products.entities.Product")
    def test_should_add_commit_and_refresh_the_created_object(
        self, product_instance
    ):
        creation_schema = schemas.ProductCreation(
            code=self.faker.md5(), summary=self.faker.word()
        )
        product_instance.return_value = ProductFactory(
            code=creation_schema.code, summary=creation_schema.summary
        )
        db = MagicMock()

        product = create_product(db=db, product=creation_schema)
        db.add.assert_called_with(product_instance())
        db.commit.assert_called_once()
        db.refresh.assert_called_with(product_instance())
        self.assertEqual(product_instance(), product)


class TestUpdateProduct(Test):
    def test_should_change_the_product_code_and_commit(self):
        product = schemas.ProductUpdate(code=self.faker.md5())
        db_product = ProductFactory()
        db = MagicMock()

        updated_product = update_product(
            db=db, product=product, db_product=db_product
        )

        self.assertEqual(updated_product.code, product.code)
        self.assertEqual(updated_product.summary, db_product.summary)
        db.commit.assert_called_once()

    def test_should_change_the_product_summary_when_it_is_specified_and_commit(
        self,
    ):
        product = schemas.ProductUpdate(
            code=self.faker.md5(), summary=self.faker.word()
        )
        db_product = ProductFactory()
        db = MagicMock()

        updated_product = update_product(
            db=db, product=product, db_product=db_product
        )

        self.assertEqual(updated_product.code, product.code)
        self.assertEqual(updated_product.summary, product.summary)
        db.commit.assert_called_once()


class TestDeleteProduct(Test):
    def test_delete_the_product_and_commit(self):
        product = ProductFactory()
        db = MagicMock()

        delete_product(db=db, product=product)

        db.delete.assert_called_with(product)
        db.commit.assert_called_once()
