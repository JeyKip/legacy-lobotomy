import uuid

import factory

from assignments.models import Category


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.LazyFunction(lambda: f'Fake Category #{uuid.uuid4().hex}')
