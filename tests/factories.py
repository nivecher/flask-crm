import factory
from factory.alchemy import SQLAlchemyModelFactory
from app.models import User, Donor, Donation
from app.extensions import db
from datetime import datetime, UTC
from decimal import Decimal
from werkzeug.security import generate_password_hash


class BaseFactory(SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"


class UserFactory(BaseFactory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password_hash = factory.LazyFunction(
        lambda: generate_password_hash("password")
    )

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        # Use the provided password, or a default.
        password_to_set = extracted or "password"
        self.set_password(password_to_set)



class DonorFactory(BaseFactory):
    class Meta:
        model = Donor

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    email = factory.Sequence(lambda n: f"donor{n}@example.com")
    phone = factory.Faker("phone_number")
    address = factory.Faker("address")


class DonationFactory(BaseFactory):
    class Meta:
        model = Donation

    id = factory.Sequence(lambda n: n)
    amount = factory.LazyFunction(lambda: Decimal("100.00"))
    date = factory.LazyFunction(lambda: datetime.now(UTC))
    type = "Online"
    donor = factory.SubFactory(DonorFactory)

