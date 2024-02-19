import random
from typing import Callable

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import IntegrityError, transaction

from assignments.factories import (
    AssignmentFactory, AssignmentTargetFactory, CategoryFactory, ImageBlockFactory, OptionFactory, QuestionBlockFactory,
    TextBlockFactory, VideoBlockFactory
)
from assignments.models import Assignment, AssingmentTarget, Category
from playbooks.factories import (
    PlaybookAssignmentFactory, PlaybookImageBlockFactory, PlaybookOptionFactory, PlaybookQuestionBlockFactory,
    PlaybookTextBlockFactory, PlaybookVideoBlockFactory
)
from playbooks.models import PlaybookAssignment
from users.factories import UserFactory

User = get_user_model()


def _generate_records(records_count: int, generator: Callable, starting_number: int = 1) -> int:
    success_count = 0
    fails_count = 0

    record_number = starting_number

    while success_count < records_count and fails_count < 10:
        try:
            generator(record_number)
            success_count += 1
        except IntegrityError:
            fails_count += 1

        record_number += 1

    return success_count


class GenerateUsersCommandHandler:
    @staticmethod
    def add_arguments(parser):
        parser.add_argument(
            '--users-count',
            nargs='?',
            type=int,
            help='A number of users which should be generated. Do not use it if not needed to generate users.'
        )
        parser.add_argument(
            '--users-starting-number',
            nargs='?',
            type=int,
            const=1,
            default=1,
            help='The starting number that will be used to number all generated users.'
        )
        parser.add_argument(
            '--users-email-template',
            nargs='?',
            type=str,
            const='legacy-lobotomy-user-{}@fake.com',
            default='legacy-lobotomy-user-{}@fake.com',
            help='A desired email template that will be used for all generated users. It must contain a placeholder '
                 'for putting a unique number.'
        )

    def __init__(
            self,
            users_count,
            users_starting_number,
            users_email_template,
            success_cb,
            **kwargs
    ):
        self._users_count = users_count
        self._users_starting_number = users_starting_number
        self._users_email_template = users_email_template
        self._success_cb = success_cb

    def execute(self):
        if self._users_count is not None and self._users_count > 0:
            def generate_user(n):
                user = UserFactory(email=self._users_email_template.format(n))
                self._success_cb(f'User with email {user.email} was generated successfully')

            users_generated = _generate_records(self._users_count, generate_user, self._users_starting_number)

            self._success_cb(f'Users generated: {users_generated}.')
        else:
            self._success_cb('Users generating was skipped.')


class GenerateCategoriesCommandHandler:
    @staticmethod
    def add_arguments(parser):
        parser.add_argument(
            '--categories-count',
            nargs='?',
            type=int,
            help='A number of assignment categories which should be generated. Do not use it if not needed '
                 'to generate categories.'
        )
        parser.add_argument(
            '--categories-starting-number',
            nargs='?',
            type=int,
            const=1,
            default=1,
            help='The starting number that will be used to number all generated categories.'
        )
        parser.add_argument(
            '--categories-name-template',
            nargs='?',
            type=str,
            const='Category #{}',
            default='Category #{}',
            help='A desired category name template that will be used for all generated categories. It must contain '
                 'a placeholder for putting a unique number.'
        )

    def __init__(
            self,
            categories_count,
            categories_starting_number,
            categories_name_template,
            success_cb,
            **kwargs
    ):
        self._categories_count = categories_count
        self._categories_starting_number = categories_starting_number
        self._categories_name_template = categories_name_template
        self._success_cb = success_cb

    def execute(self):
        if self._categories_count is not None and self._categories_count > 0:
            def generate_category(n):
                category = CategoryFactory(name=self._categories_name_template.format(n))
                self._success_cb(f'Category with name {category.name} was generated successfully')

            categories_generated = _generate_records(
                self._categories_count, generate_category, self._categories_starting_number
            )

            self._success_cb(f'Categories generated: {categories_generated}.')
        else:
            self._success_cb('Categories generating was skipped.')


class GenerateAssignmentTargetsCommandHandler:
    @staticmethod
    def add_arguments(parser):
        parser.add_argument(
            '--assignment-targets-count',
            nargs='?',
            type=int,
            help='A number of assignment targets which should be generated. Do not use it if not needed '
                 'to generate assignment targets.'
        )
        parser.add_argument(
            '--assignment-targets-starting-number',
            nargs='?',
            type=int,
            const=1,
            default=1,
            help='The starting number that will be used to number all generated assignment targets.'
        )
        parser.add_argument(
            '--assignment-targets-name-template',
            nargs='?',
            type=str,
            const='Assignment target #{}',
            default='Assignment target #{}',
            help='A desired assignment target name template that will be used for all generated assignment targets. '
                 'It must contain a placeholder for putting a unique number.'
        )

    def __init__(
            self,
            assignment_targets_count,
            assignment_targets_starting_number,
            assignment_targets_name_template,
            success_cb,
            **kwargs
    ):
        self._assignment_targets_count = assignment_targets_count
        self._assignment_targets_starting_number = assignment_targets_starting_number
        self._assignment_targets_name_template = assignment_targets_name_template
        self._success_cb = success_cb

    def execute(self):
        if self._assignment_targets_count is not None and self._assignment_targets_count > 0:
            def generate_assignment_target(n):
                assignment_target = AssignmentTargetFactory(name=self._assignment_targets_name_template.format(n))
                self._success_cb(f'Assignment target with name {assignment_target.name} was generated successfully')

            assignment_targets_generated = _generate_records(
                self._assignment_targets_count, generate_assignment_target, self._assignment_targets_starting_number
            )

            self._success_cb(f'Assignment targets generated: {assignment_targets_generated}.')
        else:
            self._success_cb('Assignment targets generating was skipped.')


class GenerateAssignmentsCommandHandler:
    @staticmethod
    def add_arguments(parser):
        parser.add_argument(
            '--assignments-count',
            nargs='?',
            type=int,
            help='A number of assignments which should be generated. Do not use it if not needed to generate '
                 'assignments.'
        )
        parser.add_argument(
            '--assignments-starting-number',
            nargs='?',
            type=int,
            const=1,
            default=1,
            help='The starting number that will be used to number all generated assignments.'
        )
        parser.add_argument(
            '--assignments-name-template',
            nargs='?',
            type=str,
            const='Assignment #{}',
            default='Assignment #{}',
            help='A desired assignment name template that will be used for all generated assignments. '
                 'It must contain a placeholder for putting a unique number.'
        )

    def __init__(
            self,
            assignments_count,
            assignments_starting_number,
            assignments_name_template,
            success_cb,
            **kwargs
    ):
        self._assignments_count = assignments_count
        self._assignments_starting_number = assignments_starting_number
        self._assignments_name_template = assignments_name_template
        self._success_cb = success_cb

    def execute(self):
        if self._assignments_count is not None and self._assignments_count > 0:
            assignment_categories = list(Category.objects.all())
            assignment_targets = list(AssingmentTarget.objects.all())

            assignments_generated = _generate_records(
                self._assignments_count,
                lambda n: self._generate_assignment(n, assignment_categories, assignment_targets),
                self._assignments_starting_number
            )

            self._success_cb(f'Assignments generated: {assignments_generated}.')
        else:
            self._success_cb('Assignments generating was skipped.')

    def _generate_assignment(self, n, assignment_categories, assignment_targets):
        def generate_question_block(**kwargs):
            options_count = random.randint(3, 6)
            correct_option_index = random.randint(0, options_count - 1)
            question = QuestionBlockFactory(**kwargs)

            for option_index in range(options_count):
                OptionFactory(question=question, is_correct=correct_option_index == option_index)

        assignment_block_factories = [TextBlockFactory, ImageBlockFactory, VideoBlockFactory, generate_question_block]

        with transaction.atomic():
            assignment_blocks_count = random.randint(2, 5)
            assignment = AssignmentFactory(
                category=random.choice(assignment_categories),
                target=random.choice(assignment_targets),
                name=self._assignments_name_template.format(n)
            )

            for _ in range(assignment_blocks_count):
                assignment_block_factory = random.choice(assignment_block_factories)
                assignment_block_factory(block__assignment=assignment)

            self._success_cb(f'Assignment with name {assignment.name} was generated successfully')


class GeneratePlaybookAssignmentsCommandHandler:
    @staticmethod
    def add_arguments(parser):
        parser.add_argument(
            '--generate-playbook-assignments',
            action='store_true',
            help='A flag that shows if playbook assignments should be generated. If missed, no playbook assignments '
                 'will be generated.'
        )

    def __init__(
            self,
            generate_playbook_assignments,
            success_cb,
            **kwargs
    ):
        self._generate_playbook_assignments = generate_playbook_assignments
        self._success_cb = success_cb

    def execute(self):
        if self._generate_playbook_assignments:
            assignment_categories = list(Category.objects.all())

            for user in User.objects.filter(is_superuser=False).iterator(chunk_size=500):
                for _ in range(random.randint(5, 50)):
                    self._generate_playbook_assignment(user, assignment_categories)

            self._success_cb('Playbook assignments generated.')
        else:
            self._success_cb('Playbook assignments generating was skipped.')

    def _generate_playbook_assignment(self, user, assignment_categories):
        def generate_question_block(**kwargs):
            options_count = random.randint(3, 6)
            correct_option_index = random.randint(0, options_count - 1)
            question = PlaybookQuestionBlockFactory(**kwargs)

            for option_index in range(options_count):
                PlaybookOptionFactory(question=question, is_correct=correct_option_index == option_index)

        assignment_block_factories = [
            PlaybookTextBlockFactory,
            PlaybookImageBlockFactory,
            PlaybookVideoBlockFactory,
            generate_question_block
        ]

        with transaction.atomic():
            assignment_blocks_count = random.randint(2, 5)
            assignment = PlaybookAssignmentFactory(user=user, category=random.choice(assignment_categories))

            for _ in range(assignment_blocks_count):
                assignment_block_factory = random.choice(assignment_block_factories)
                assignment_block_factory(block__assignment=assignment)

            self._success_cb(f'Playbook assignment with name {assignment.name} was generated successfully')


class CleanDatabaseCommandHandler:
    @staticmethod
    def add_arguments(parser):
        parser.add_argument(
            '--clean-database',
            action='store_true',
            help='A flag that shows if all the data in the database should be cleaned out before generating data.'
                 ' If missed, existing data will not be touched.'
        )

    def __init__(
            self,
            clean_database,
            success_cb,
            **kwargs
    ):
        self._clean_database = clean_database
        self._success_cb = success_cb

    def execute(self):
        if self._clean_database:
            Assignment.objects.all().delete()
            AssingmentTarget.objects.all().delete()
            PlaybookAssignment.objects.all().delete()
            Category.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()

            self._success_cb('Database was cleaned successfully.')
        else:
            self._success_cb('Database cleaning was skipped.')


class Command(BaseCommand):
    handlers = [
        CleanDatabaseCommandHandler,
        GenerateUsersCommandHandler,
        GenerateCategoriesCommandHandler,
        GenerateAssignmentTargetsCommandHandler,
        GenerateAssignmentsCommandHandler,
        GeneratePlaybookAssignmentsCommandHandler,
    ]
    help = 'Populates a default database with test data'

    def add_arguments(self, parser):
        for handler_cls in self.handlers:
            handler_cls.add_arguments(parser)

    def handle(self, *args, **options):
        for handler_cls in self.handlers:
            handler = handler_cls(**options, success_cb=self._success_callback)
            handler.execute()

    def _success_callback(self, message):
        self.stdout.write(self.style.SUCCESS(message))
