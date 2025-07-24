import factory

from assignments.models import TextBlock


class TextBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TextBlock

    # This property must be provided when creating a text block.
    block = None
    text = factory.Faker('paragraph')
