import factory

from playbooks.models import PlaybookImageBlock


class PlaybookImageBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlaybookImageBlock

    # This property must be provided when creating an image block.
    block = None
    image = factory.django.ImageField()
