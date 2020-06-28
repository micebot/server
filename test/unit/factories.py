import factory

from server.db.entities import Product, Order


class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    id = factory.Sequence(lambda n: n)
    code = factory.Faker("md5")
    summary = factory.Faker("sentence")
    taken = factory.Faker("boolean")
    taken_at = factory.LazyAttribute(
        lambda obj: factory.Faker(
            "date_time_between", start_date="-5d", end_date="now"
        ).generate()
        if obj.taken
        else None
    )


class OrderFactory(factory.Factory):
    class Meta:
        model = Order

    id = factory.Sequence(lambda n: n)
    mod_id = factory.Faker("uuid4")
    mod_display_name = factory.Faker("username")
    owner_display_name = factory.Faker("username")
    requested_at = factory.Faker(
        "date_time_between", start_date="-30d", end_date="-10d"
    )
    product_id = factory.Faker("pyint")
    product = factory.SubFactory(Product)