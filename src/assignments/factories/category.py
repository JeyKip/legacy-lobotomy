import uuid

import factory

from assignments.factories.providers import CategoryProvider
from assignments.models import Category
from libs.factory.django import RetryableDjangoModelFactory

# Register the custom provider
factory.Faker.add_provider(CategoryProvider)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.LazyFunction(lambda: f'Fake Category #{uuid.uuid4().hex}')


class RealisticCategoryFactory(RetryableDjangoModelFactory, CategoryFactory):
    class Meta:
        model = Category

    name = factory.Faker('category_name')
