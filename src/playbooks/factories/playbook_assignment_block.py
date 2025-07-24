import factory

from assignments.models import AssignmentBlock
from playbooks.models import PlaybookAssignmentBlock
from .playbook_image_block import PlaybookImageBlockFactory
from .playbook_question_block import PlaybookQuestionBlockFactory
from .playbook_text_block import PlaybookTextBlockFactory
from .playbook_video_block import PlaybookVideoBlockFactory

playbook_block_factories = {
    'Text': PlaybookTextBlockFactory,
    'Image': PlaybookImageBlockFactory,
    'Video': PlaybookVideoBlockFactory,
    'Question': PlaybookQuestionBlockFactory,
}


class PlaybookAssignmentBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlaybookAssignmentBlock

    # This property must be provided when creating an assignment block.
    assignment = None
    name = factory.Faker('sentence', nb_words=3)
    type_of_block = factory.Faker('random_element', elements=[item[0] for item in AssignmentBlock.TYPE_CHOICES])

    @factory.post_generation
    def create_block_of_target_type(self, create, extracted, **kwargs):
        if not create:
            return

        playbook_block_factories[self.type_of_block](block=self)
