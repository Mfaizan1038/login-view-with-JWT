import factory
from accounts.models import User

class UserFactory(factory.django.DjangoModelFactory):
    """Factory for creating User instances for tests."""
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    phone_number = factory.Faker("phone_number")
    password = factory.PostGenerationMethodCall("set_password", "password123")
