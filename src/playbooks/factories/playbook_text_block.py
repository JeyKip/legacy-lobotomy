import factory

from playbooks.models import PlaybookTextBlock


class PlaybookTextBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlaybookTextBlock

    # This property must be provided when creating a text block.
    block = None
    text = factory.Faker('paragraph')
