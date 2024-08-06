import uuid

import factory
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.LazyFunction(lambda: f'fake-user-{uuid.uuid4().hex}@fakemail.com')
    password = factory.django.Password('123456')
