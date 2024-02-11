import factory
from django.conf import settings
from django.db.models.signals import post_save

from assignments.factories.assignment import AssignmentFactory
from assignments.models import AssignmentBlock, ImageBlock, Option, QuestionBlock, TextBlock, VideoBlock


# We don't want the prevent_empty_blocks signal handler to be called because it prevents creating empty objects of the
# AssignmentBlock type. That's why we need to mute the post_save signal for the underlined model.
@factory.django.mute_signals(post_save)
class AssignmentBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AssignmentBlock

    name = factory.Faker('sentence', nb_words=3)
    type_of_block = factory.Faker('random_element', elements=[item[0] for item in AssignmentBlock.TYPE_CHOICES])
    assignment = factory.SubFactory(AssignmentFactory)


class TextBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TextBlock

    block = factory.SubFactory(AssignmentBlockFactory)
    text = factory.Faker('paragraph')


class ImageBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ImageBlock

    block = factory.SubFactory(AssignmentBlockFactory)
    image = factory.django.ImageField()


class VideoBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VideoBlock

    block = factory.SubFactory(AssignmentBlockFactory)
    video = factory.django.FileField(from_path=settings.ROOT_DIR / 'static/testing-assets/video-sample.mp4')


class QuestionBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = QuestionBlock

    block = factory.SubFactory(AssignmentBlockFactory)
    text = factory.Faker('paragraph')


class OptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Option

    text = factory.Faker('paragraph')
    tip = factory.Faker('paragraph')
    # The model validation doesn't allow to save multiple options with is_correct value equal to True.
    # So it's better to always keep this flag equal to False in order to prevent validation errors while saving.
    is_correct = False
    question = factory.SubFactory(QuestionBlockFactory)
