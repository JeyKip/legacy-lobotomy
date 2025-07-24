import pytest
from django.contrib.auth import get_user_model
from django.core.management import CommandError, call_command

from users.models import Team

User = get_user_model()


@pytest.mark.django_db
class TestSeedUsers:
    def test_when_there_are_no_teams_then_error_should_be_thrown(self):
        with pytest.raises(CommandError) as exc_info:
            call_command('seed_users')

        assert str(exc_info.value) == 'The team does not exist.'

    def test_when_team_with_provided_id_does_not_exist_then_error_should_be_thrown(self, team):
        with pytest.raises(CommandError) as exc_info:
            call_command('seed_users', team_id=team.pk + 1)

        assert str(exc_info.value) == 'The team does not exist.'

    def test_when_team_id_is_not_provided_then_random_team_should_be_selected(self, team_factory):
        teams_total_count = 5
        teams = team_factory.create_batch(teams_total_count)
        call_command('seed_users')

        existing_team_ids = {team.pk for team in teams}
        used_team_ids = {user.team_id for user in User.objects.all()}

        # Since the team selection is randomized, we can only verify that more than one team was used.
        # There's still a small chance that all 10 assignments receive the same team,
        # but the probability is low enough to be negligible.
        assert len(used_team_ids) > 1

        # Ensure that only existing categories are used and no new categories are created.
        assert used_team_ids - existing_team_ids == set()

    @pytest.mark.parametrize('team_id', [-10, 0, 0.5, 'invalid'])
    def test_when_team_id_argument_is_invalid_then_error_should_be_thrown(self, team_id):
        with pytest.raises(CommandError) as exc_info:
            call_command('seed_users', team_id=team_id)

        assert str(exc_info.value) == 'The --team-id argument must be an integer value greater than or equal to 1.'

    @pytest.mark.parametrize('count', [-10, 0, 0.5, 'invalid'])
    def test_when_count_argument_is_invalid_then_error_should_be_thrown(self, count, team):
        with pytest.raises(CommandError) as exc_info:
            call_command('seed_users', team_id=team.pk, count=count)

        assert str(exc_info.value) == 'The --count argument must be an integer value greater than or equal to 1.'

    def test_when_count_argument_is_not_provided_then_10_users_should_be_created(self, team):
        call_command('seed_users', team_id=team.pk)

        assert User.objects.count() == 10

    @pytest.mark.parametrize('count', [1, 5, 12])
    def test_when_count_argument_is_provided_then_requested_number_of_users_should_be_created(self, count, team):
        call_command('seed_users', team_id=team.pk, count=count)

        assert User.objects.count() == count

    def test_when_team_id_provided_then_all_users_should_be_assigned_to_the_same_team(self, team):
        call_command('seed_users', team_id=team.pk)

        user_team_ids = {user.team_id for user in User.objects.all()}

        assert user_team_ids == {team.pk}

        # Verify that new teams were not created.
        assert Team.objects.count() == 1

    @pytest.mark.parametrize('count', [1, 5, 12])
    def test_when_user_is_created_then_its_id_should_be_written_to_standard_output(self, count, team, capsys):
        call_command('seed_users', team_id=team.pk, count=count)

        captured_output = capsys.readouterr().out.strip()
        captured_user_ids = {int(user_id) for user_id in captured_output.split(',')}

        assert len(captured_user_ids) == count
