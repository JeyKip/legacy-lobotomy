import random
import uuid

import factory

from assignments.factories import CategoryFactory
from playbooks.models import PlaybookAssignment
from users.factories import RegularUserFactory
from .playbook_assignment_block import PlaybookAssignmentBlockFactory


class PlaybookAssignmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlaybookAssignment

    user = factory.SubFactory(RegularUserFactory)
    name = factory.LazyFunction(lambda: f'Fake Assignment #{uuid.uuid4().hex}')
    description = factory.Faker('paragraph')
    image = factory.django.ImageField()
    points = factory.Faker('pyint', min_value=0, max_value=100)
    time = factory.Faker('pyint', min_value=10, max_value=300)
    category = factory.SubFactory(CategoryFactory)
    priority = factory.Faker('pyint', min_value=0, max_value=25)
    blocks = factory.RelatedFactoryList(
        PlaybookAssignmentBlockFactory,
        factory_related_name='assignment',
        size=lambda: random.randint(1, 6)
    )
