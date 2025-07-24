from django.core.management import BaseCommand, CommandError

from users.factories import TeamFactory


class Command(BaseCommand):
    help = 'Seed fake teams.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            required=False,
            type=int,
            default=10,
            help='The number of teams which should be created.'
        )

    def handle(self, count, *args, **options):
        if not isinstance(count, int) or count < 1:
            raise CommandError('The --count argument must be an integer value greater than or equal to 1.')

        created_teams = TeamFactory.create_batch(count)
        created_teams_output = ','.join([str(team.pk) for team in created_teams])
        self.stdout.write(created_teams_output)
