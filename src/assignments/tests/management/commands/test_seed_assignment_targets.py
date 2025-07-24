import pytest
from django.core.management import CommandError, call_command

from assignments.models import AssingmentTarget


@pytest.mark.django_db
class TestSeedAssignmentTargets:
    def test_when_count_argument_is_not_provided_then_5_assignment_targets_should_be_created(self):
        call_command('seed_assignment_targets')

        assert AssingmentTarget.objects.count() == 5

    @pytest.mark.parametrize('count', [-10, 0, 0.5, 'invalid'])
    def test_when_count_argument_is_invalid_then_error_should_be_thrown(self, count):
        with pytest.raises(CommandError) as exc_info:
            call_command('seed_assignment_targets', count=count)

        assert str(exc_info.value) == 'The --count argument must be an integer value greater than or equal to 1.'

    @pytest.mark.parametrize('count', [1, 5, 12])
    def test_when_count_argument_is_provided_then_requested_number_of_assignment_targets_should_be_created(self, count):
        call_command('seed_assignment_targets', count=count)

        assert AssingmentTarget.objects.count() == count

    @pytest.mark.parametrize('count', [1, 5, 12])
    def test_when_assignment_target_is_created_then_its_id_should_be_written_to_standard_output(self, count, capsys):
        call_command('seed_assignment_targets', count=count)

        captured_output = capsys.readouterr().out.strip()
        captured_assignment_target_ids = {int(target_id) for target_id in captured_output.split(',')}

        assert len(captured_assignment_target_ids) == count
