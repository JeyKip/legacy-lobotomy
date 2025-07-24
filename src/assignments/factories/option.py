import factory

from assignments.models import Option


class OptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Option

    # This property must be provided when creating an option.
    question = None
    text = factory.Faker('paragraph')
    tip = factory.Faker('paragraph')
    is_correct = False
