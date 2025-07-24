from django.core.management import BaseCommand, CommandError

from assignments.factories import CategoryFactory


class Command(BaseCommand):
    help = 'Seed fake categories.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            required=False,
            type=int,
            default=5,
            help='The number of categories which should be created.'
        )

    def handle(self, count, *args, **options):
        if not isinstance(count, int) or count < 1:
            raise CommandError('The --count argument must be an integer value greater than or equal to 1.')

        categories = CategoryFactory.create_batch(count)
        category_ids = ','.join(str(category.pk) for category in categories)
        self.stdout.write(category_ids)
