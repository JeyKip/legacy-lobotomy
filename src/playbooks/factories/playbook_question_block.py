import random

import factory

from playbooks.factories.playbook_option import PlaybookOptionFactory
from playbooks.models import PlaybookQuestionBlock


class PlaybookQuestionBlockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlaybookQuestionBlock

    # This property must be provided when creating a question block.
    block = None
    text = factory.Faker('paragraph')
    options = factory.RelatedFactoryList(PlaybookOptionFactory, 'question', lambda: random.randint(3, 6))

    @factory.post_generation
    def select_correct_option(self, create, extracted, **kwargs):
        if not create:
            return

        options = list(self.options.all())

        # Mark a random option as correct.
        correct_option = random.choice(options)
        correct_option.is_correct = True
        correct_option.save()
