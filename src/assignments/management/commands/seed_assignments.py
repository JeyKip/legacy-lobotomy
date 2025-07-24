from django.core.management import BaseCommand, CommandError

from assignments.factories import AssignmentFactory
from assignments.models import AssingmentTarget, Category


class Command(BaseCommand):
    help = 'Seed fake assignments.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            required=False,
            type=int,
            default=10,
            help='The number of assignments which should be created.'
        )
        parser.add_argument(
            '--category-id',
            required=False,
            type=int,
            help='A category to which the assignment should be linked.'
        )
        parser.add_argument(
            '--target-id',
            required=False,
            type=int,
            help='An assignment target to which the assignment should be linked.'
        )

    def handle(self, count, *args, **options):
        if not isinstance(count, int) or count < 1:
            raise CommandError('The --count argument must be an integer value greater than or equal to 1.')

        try:
            category = self._parse_category(**options)
            assignment_target = self._parse_assignment_target(**options)

            for _ in range(count):
                AssignmentFactory(
                    category=category or self._fetch_random_category(),
                    target=assignment_target or self._fetch_random_assignment_target(),
                )
        except Category.DoesNotExist:
            raise CommandError('The category does not exist.')
        except AssingmentTarget.DoesNotExist:
            raise CommandError('The assignment target does not exist.')

    def _parse_category(self, **options):
        category_id = options.get('category_id')

        if category_id is None:
            return None

        if not isinstance(category_id, int) or category_id < 1:
            raise CommandError('The --category-id argument must be an integer value greater than or equal to 1.')

        return Category.objects.get(pk=category_id)

    def _fetch_random_category(self):
        return Category.objects.order_by('?')[:1].get()

    def _parse_assignment_target(self, **options):
        target_id = options.get('target_id')

        if target_id is None:
            return None

        if not isinstance(target_id, int) or target_id < 1:
            raise CommandError('The --target-id argument must be an integer value greater than or equal to 1.')

        return AssingmentTarget.objects.get(pk=target_id)

    def _fetch_random_assignment_target(self):
        return AssingmentTarget.objects.order_by('?')[:1].get()
