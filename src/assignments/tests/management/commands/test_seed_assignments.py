import pytest
from django.core.management import CommandError, call_command

from assignments.models import Assignment, AssingmentTarget, Category


@pytest.mark.django_db
class TestSeedAssignments:
    def test_when_there_are_no_categories_then_error_should_be_thrown(self):
        with pytest.raises(CommandError) as exc_info:
            call_command('seed_assignments')

        assert str(exc_info.value) == 'The category does not exist.'

    def test_when_category_with_provided_id_does_not_exist_then_error_should_be_thrown(self, category):
        with pytest.raises(CommandError) as exc_info:
            call_command('seed_assignments', category_id=category.id + 1)

        assert str(exc_info.value) == 'The category does not exist.'

    @pytest.mark.parametrize('category_id', [-10, 0, 0.5, 'invalid'])
    def test_when_category_id_argument_is_invalid_then_error_should_be_thrown(self, category_id):
        with pytest.raises(CommandError) as exc_info:
            call_command('seed_assignments', category_id=category_id)

        assert str(exc_info.value) == 'The --category-id argument must be an integer value greater than or equal to 1.'

    def test_when_there_are_no_assignment_targets_then_error_should_be_thrown(self, category):
        with pytest.raises(CommandError) as exc_info:
            call_command('seed_assignments', category_id=category.id)

        assert str(exc_info.value) == 'The assignment target does not exist.'

    def test_when_assignment_target_with_provided_id_does_not_exist_then_error_should_be_thrown(
            self, category, assignment_target
    ):
        with pytest.raises(CommandError) as exc_info:
            call_command('seed_assignments', category_id=category.id, target_id=assignment_target.id + 1)

        assert str(exc_info.value) == 'The assignment target does not exist.'

    @pytest.mark.parametrize('target_id', [-10, 0, 0.5, 'invalid'])
    def test_when_assignment_target_id_argument_is_invalid_then_error_should_be_thrown(self, category, target_id):
        with pytest.raises(CommandError) as exc_info:
            call_command('seed_assignments', category_id=category.id, target_id=target_id)

        assert str(exc_info.value) == 'The --target-id argument must be an integer value greater than or equal to 1.'

    def test_when_count_argument_is_not_provided_then_10_assignments_should_be_created(
            self, category, assignment_target
    ):
        call_command('seed_assignments')

        assert Assignment.objects.count() == 10

    @pytest.mark.parametrize('count', [-10, 0, 0.5, 'invalid'])
    def test_when_count_argument_is_invalid_then_error_should_be_thrown(self, category, assignment_target, count):
        with pytest.raises(CommandError) as exc_info:
            call_command('seed_assignments', count=count)

        assert str(exc_info.value) == 'The --count argument must be an integer value greater than or equal to 1.'

    @pytest.mark.parametrize('count', [1, 5, 12])
    def test_when_count_argument_is_provided_then_requested_number_of_assignments_should_be_created(
            self, category, assignment_target, count
    ):
        call_command('seed_assignments', count=count)

        assert Assignment.objects.count() == count

    def test_when_category_is_not_provided_then_one_of_existing_categories_should_be_used(
            self, assignment_target, category_factory
    ):
        categories_count = 5
        categories = category_factory.create_batch(categories_count)
        call_command('seed_assignments')

        existing_category_ids = {category.pk for category in categories}
        used_category_ids = {assignment.category_id for assignment in Assignment.objects.all()}

        # Since the category selection is randomized, we can only verify that more than one category was used.
        # There's still a small chance that all 10 assignments receive the same category,
        # but the probability is low enough to be negligible.
        assert len(used_category_ids) > 1

        # Ensure that only existing categories are used and no new categories are created.
        assert used_category_ids - existing_category_ids == set()

    def test_when_category_id_provided_then_all_assignments_should_be_assigned_to_the_same_category(
            self, category, assignment_target
    ):
        call_command('seed_assignments', category_id=category.pk)

        used_category_ids = {assignment.category_id for assignment in Assignment.objects.all()}

        assert used_category_ids == {category.pk}

        # Verify that new categories were not created.
        assert Category.objects.count() == 1

    def test_when_assignment_target_is_not_provided_then_one_of_existing_targets_should_be_used(
            self, category, assignment_target_factory
    ):
        assignment_targets_count = 5
        assignment_targets = assignment_target_factory.create_batch(assignment_targets_count)
        call_command('seed_assignments')

        existing_assignment_target_ids = {target.pk for target in assignment_targets}
        used_assignment_target_ids = {assignment.target_id for assignment in Assignment.objects.all()}

        # Since the target selection is randomized, we can only verify that more than one target was used.
        # There's still a small chance that all 10 assignments receive the same target,
        # but the probability is low enough to be negligible.
        assert len(used_assignment_target_ids) > 1

        # Ensure that only existing targets are used and no new categories are created.
        assert used_assignment_target_ids - existing_assignment_target_ids == set()

    def test_when_assignment_target_provided_then_all_assignments_should_be_assigned_to_the_same_target(
            self, category, assignment_target
    ):
        call_command('seed_assignments', target_id=assignment_target.pk)

        used_assignment_target_ids = {assignment.target_id for assignment in Assignment.objects.all()}

        assert used_assignment_target_ids == {assignment_target.pk}

        # Verify that new assignment targets were not created.
        assert AssingmentTarget.objects.count() == 1
