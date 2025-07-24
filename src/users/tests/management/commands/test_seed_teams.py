import pytest
from django.core.management import CommandError, call_command

from users.models import Team


@pytest.mark.django_db
class TestSeedTeams:
    def test_when_count_argument_is_not_provided_then_10_teams_should_be_created(self):
        call_command('seed_teams')

        assert Team.objects.count() == 10

    @pytest.mark.parametrize('count', [-10, 0, 0.5, 'invalid'])
    def test_when_count_argument_is_invalid_then_error_should_be_thrown(self, count):
        with pytest.raises(CommandError) as exc_info:
            call_command('seed_teams', count=count)

        assert str(exc_info.value) == 'The --count argument must be an integer value greater than or equal to 1.'

    @pytest.mark.parametrize('count', [1, 5, 12])
    def test_when_count_argument_is_provided_then_requested_number_of_teams_should_be_created(self, count):
        call_command('seed_teams', count=count)

        assert Team.objects.count() == count

    @pytest.mark.parametrize('count', [1, 5, 12])
    def test_when_team_is_created_then_its_id_should_be_written_to_standard_output(self, count, capsys):
        call_command('seed_teams', count=count)

        captured_output = capsys.readouterr().out.strip()
        captured_team_ids = {int(team_id) for team_id in captured_output.split(',')}

        assert len(captured_team_ids) == count
