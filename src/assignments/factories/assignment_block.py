import factory
from django.db.models.signals import post_save

from assignments.models import AssignmentBlock
from .image_block import ImageBlockFactory
from .question_block import QuestionBlockFactory
from .text_block import TextBlockFactory
from .video_block import VideoBlockFactory

block_factories = {
    'Text': TextBlockFactory,
    'Image': ImageBlockFactory,
    'Video': VideoBlockFactory,
    'Question': QuestionBlockFactory,
}


# We don't want the prevent_empty_blocks signal handler-added by the development team as a workaround-to be triggered,
# as it prevents the creation of empty AssignmentBlock instances. For this reason, we need to mute the post_save signal
# for the corresponding model.
@factory.django.mute_signals(post_save)
class AssignmentBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AssignmentBlock

    # This property must be provided when creating an assignment block.
    assignment = None
    name = factory.Faker('sentence', nb_words=3)
    type_of_block = factory.Faker('random_element', elements=[item[0] for item in AssignmentBlock.TYPE_CHOICES])

    @factory.post_generation
    def create_block_of_target_type(self, create, extracted, **kwargs):
        if not create:
            return

        block_factories[self.type_of_block](block=self)
