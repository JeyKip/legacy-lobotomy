import pytest
from django.core.management import CommandError, call_command

from assignments.models import Category


@pytest.mark.django_db
class TestSeedCategories:
    def test_when_count_argument_is_not_provided_then_5_categories_should_be_created(self):
        call_command('seed_categories')

        assert Category.objects.count() == 5

    @pytest.mark.parametrize('count', [-10, 0, 0.5, 'invalid'])
    def test_when_count_argument_is_invalid_then_error_should_be_thrown(self, count):
        with pytest.raises(CommandError) as exc_info:
            call_command('seed_categories', count=count)

        assert str(exc_info.value) == 'The --count argument must be an integer value greater than or equal to 1.'

    @pytest.mark.parametrize('count', [1, 5, 12])
    def test_when_count_argument_is_provided_then_requested_number_of_categories_should_be_created(self, count):
        call_command('seed_categories', count=count)

        assert Category.objects.count() == count

    @pytest.mark.parametrize('count', [1, 5, 12])
    def test_when_category_is_created_then_its_id_should_be_written_to_standard_output(self, count, capsys):
        call_command('seed_categories', count=count)

        captured_output = capsys.readouterr().out.strip()
        captured_category_ids = {int(category_id) for category_id in captured_output.split(',')}

        assert len(captured_category_ids) == count
