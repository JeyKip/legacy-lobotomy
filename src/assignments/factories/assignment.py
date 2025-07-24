import random
import uuid

import factory

from assignments.models import Assignment
from .assignment_block import AssignmentBlockFactory
from .assignment_target import AssignmentTargetFactory
from .category import CategoryFactory


class AssignmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Assignment

    name = factory.LazyFunction(lambda: f'Fake Assignment #{uuid.uuid4().hex}')
    description = factory.Faker('paragraph')
    image = factory.django.ImageField()
    points = factory.Faker('pyint', min_value=0, max_value=100)
    time = factory.Faker('pyint', min_value=10, max_value=300)
    category = factory.SubFactory(CategoryFactory)
    target = factory.SubFactory(AssignmentTargetFactory)
    priority = factory.Faker('pyint', min_value=0, max_value=25)
    blocks = factory.RelatedFactoryList(
        AssignmentBlockFactory,
        factory_related_name='assignment',
        size=lambda: random.randint(1, 6)
    )
