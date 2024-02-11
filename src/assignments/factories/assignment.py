import factory

from assignments.factories.assignment_target import AssignmentTargetFactory
from assignments.factories.category import CategoryFactory
from assignments.models import Assignment


class AssignmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Assignment

    name = factory.Sequence(lambda n: f'Assignment #{n + 1}')
    description = factory.Faker('paragraph')
    image = factory.django.ImageField()
    points = factory.Faker('pyint', min_value=0, max_value=100)
    time = factory.Faker('pyint', min_value=10, max_value=300)
    category = factory.SubFactory(CategoryFactory)
    target = factory.SubFactory(AssignmentTargetFactory)
    priority = factory.Faker('pyint', min_value=0, max_value=25)
