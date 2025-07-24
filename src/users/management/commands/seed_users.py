from django.core.management import BaseCommand, CommandError

from users.factories import RegularUserFactory
from users.models import Team


class Command(BaseCommand):
    help = 'Seed fake users.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--team-id',
            required=False,
            type=int,
            help='The team ID the users should be assigned to.'
        )

        parser.add_argument(
            '--count',
            required=False,
            type=int,
            default=10,
            help='The number of users which should be created.'
        )

    def handle(self, count, *args, **options):
        if not isinstance(count, int) or count < 1:
            raise CommandError('The --count argument must be an integer value greater than or equal to 1.')

        try:
            # Retrieve a team if team id is provided.
            team = self._parse_team(**options)

            # If a team wasn't provided, assign the user to a random team.
            created_users = [RegularUserFactory(team=team or self._fetch_random_team()) for _ in range(count)]
        except Team.DoesNotExist:
            raise CommandError('The team does not exist.')

        created_users_output = ','.join([str(user.pk) for user in created_users])
        self.stdout.write(created_users_output)

    def _parse_team(self, **options):
        team_id = options.get('team_id')

        # Since we don't have a default value for this argument, we want to validate it only when it's passed.
        if team_id is None:
            return None

        if not isinstance(team_id, int) or team_id < 1:
            raise CommandError('The --team-id argument must be an integer value greater than or equal to 1.')

        return Team.objects.get(pk=team_id)

    def _fetch_random_team(self):
        return Team.objects.order_by('?')[:1].get()
