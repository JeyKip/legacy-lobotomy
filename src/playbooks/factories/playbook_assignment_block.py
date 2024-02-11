import factory
from django.conf import settings

from assignments.models import AssignmentBlock
from playbooks.factories.playbook_assignment import PlaybookAssignmentFactory
from playbooks.models import (
    PlaybookAssignmentBlock, PlaybookImageBlock, PlaybookOption, PlaybookQuestionBlock, PlaybookTextBlock,
    PlaybookVideoBlock
)


class PlaybookAssignmentBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlaybookAssignmentBlock

    name = factory.Faker('sentence', nb_words=3)
    type_of_block = factory.Faker('random_element', elements=[item[0] for item in AssignmentBlock.TYPE_CHOICES])
    assignment = factory.SubFactory(PlaybookAssignmentFactory)


class PlaybookTextBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlaybookTextBlock

    block = factory.SubFactory(PlaybookAssignmentBlockFactory)
    text = factory.Faker('paragraph')


class PlaybookImageBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlaybookImageBlock

    block = factory.SubFactory(PlaybookAssignmentBlockFactory)
    image = factory.django.ImageField()


class PlaybookVideoBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlaybookVideoBlock

    block = factory.SubFactory(PlaybookAssignmentBlockFactory)
    video = factory.django.FileField(from_path=settings.ROOT_DIR / 'static/testing-assets/video-sample.mp4')


class PlaybookQuestionBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlaybookQuestionBlock

    block = factory.SubFactory(PlaybookAssignmentBlockFactory)
    text = factory.Faker('paragraph')


class PlaybookOptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlaybookOption

    text = factory.Faker('paragraph')
    tip = factory.Faker('paragraph')
    is_correct = False
    question = factory.SubFactory(PlaybookQuestionBlockFactory)
