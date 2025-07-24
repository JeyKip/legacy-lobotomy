from django.core.management import BaseCommand, CommandError
from assignments.factories import AssignmentTargetFactory


class Command(BaseCommand):
    help = 'Seed fake assignment targets.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=5,
            help='The number of assignment targets which should be created.'
        )

    def handle(self, count, *args, **options):
        if not isinstance(count, int) or count < 1:
            raise CommandError('The --count argument must be an integer value greater than or equal to 1.')

        assignment_targets = AssignmentTargetFactory.create_batch(count)
        ids = ','.join(str(target.pk) for target in assignment_targets)
        self.stdout.write(ids)
