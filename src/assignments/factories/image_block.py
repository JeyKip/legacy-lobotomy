import factory

from assignments.models import ImageBlock


class ImageBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ImageBlock

    # This property must be provided when creating an image block.
    block = None
    image = factory.django.ImageField()
