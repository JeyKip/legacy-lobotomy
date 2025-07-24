from django.contrib.auth import get_user_model
from django.core.management import BaseCommand, CommandError

from assignments.models import Category
from playbooks.factories import PlaybookAssignmentFactory

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed fake playbook assignments.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            required=False,
            type=int,
            default=10,
            help='The number of playbook assignments which should be created.'
        )
        parser.add_argument(
            '--category-id',
            required=False,
            type=int,
            help='A category to which the assignment should be linked.'
        )
        parser.add_argument(
            '--user-id',
            required=False,
            type=int,
            help='A user to which the assignment should be linked.'
        )

    def handle(self, count, *args, **options):
        if not isinstance(count, int) or count < 1:
            raise CommandError('The --count argument must be an integer value greater than or equal to 1.')

        try:
            category = self._parse_category(**options)
            user = self._parse_user(**options)

            for _ in range(count):
                PlaybookAssignmentFactory(
                    category=category or self._fetch_random_category(),
                    user=user or self._fetch_random_user(),
                )
        except Category.DoesNotExist:
            raise CommandError('The category does not exist.')
        except User.DoesNotExist:
            raise CommandError('The user does not exist.')

    def _parse_category(self, **options):
        category_id = options.get('category_id')

        if category_id is None:
            return None

        if not isinstance(category_id, int) or category_id < 1:
            raise CommandError('The --category-id argument must be an integer value greater than or equal to 1.')

        return Category.objects.get(pk=category_id)

    def _fetch_random_category(self):
        return Category.objects.order_by('?')[:1].get()

    def _parse_user(self, **options):
        user_id = options.get('user_id')

        if user_id is None:
            return None

        if not isinstance(user_id, int) or user_id < 1:
            raise CommandError('The --user-id argument must be an integer value greater than or equal to 1.')

        return User.objects.get(pk=user_id)

    def _fetch_random_user(self):
        return User.objects.order_by('?')[:1].get()
