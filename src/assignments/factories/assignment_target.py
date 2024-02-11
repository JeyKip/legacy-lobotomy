import factory

from assignments.models import AssingmentTarget


class AssignmentTargetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AssingmentTarget

    name = factory.Sequence(lambda n: f'Assignment target #{n + 1}')
    min_age = factory.Faker('pyint', min_value=13, max_value=99)
    max_age = factory.Faker('pyint', min_value=factory.SelfAttribute('..min_age'), max_value=99)
    male = factory.Faker('pybool')
    female = factory.Faker('pybool')
    non_binary = factory.Faker('pybool')
    transgender = factory.Faker('pybool')
    other = factory.Faker('pybool')
    law_explorer = factory.Faker('pybool')
