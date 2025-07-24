import factory

from playbooks.models import PlaybookOption


class PlaybookOptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlaybookOption

    # This property must be provided when creating an option.
    question = None
    text = factory.Faker('paragraph')
    tip = factory.Faker('paragraph')
    is_correct = False
