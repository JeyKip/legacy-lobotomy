import pytest
from django.contrib.auth import get_user_model
from django.core.management import CommandError, call_command

from assignments.models import Category
from playbooks.models import PlaybookAssignment

User = get_user_model()


@pytest.mark.django_db
class TestSeedPlaybookAssignments:
    def test_when_there_are_no_categories_then_error_should_be_thrown(self):
        with pytest.raises(CommandError) as exc_info:
            call_command('seed_playbook_assignments')

        assert str(exc_info.value) == 'The category does not exist.'

    def test_when_category_with_provided_id_does_not_exist_then_error_should_be_thrown(self, category):
        with pytest.raises(CommandError) as exc_info:
            call_command('seed_playbook_assignments', category_id=category.id + 1)

        assert str(exc_info.value) == 'The category does not exist.'

    @pytest.mark.parametrize('category_id', [-10, 0, 0.5, 'invalid'])
    def test_when_category_id_argument_is_invalid_then_error_should_be_thrown(self, category_id):
        with pytest.raises(CommandError) as exc_info:
            call_command('seed_playbook_assignments', category_id=category_id)

        assert str(exc_info.value) == 'The --category-id argument must be an integer value greater than or equal to 1.'

    def test_when_there_are_no_users_then_error_should_be_thrown(self, category):
        with pytest.raises(CommandError) as exc_info:
            call_command('seed_playbook_assignments', category_id=category.id)

        assert str(exc_info.value) == 'The user does not exist.'

    def test_when_user_with_provided_id_does_not_exist_then_error_should_be_thrown(
            self, category, regular_user
    ):
        with pytest.raises(CommandError) as exc_info:
            call_command('seed_playbook_assignments', category_id=category.id, user_id=regular_user.id + 1)

        assert str(exc_info.value) == 'The user does not exist.'

    @pytest.mark.parametrize('user_id', [-10, 0, 0.5, 'invalid'])
    def test_when_user_id_argument_is_invalid_then_error_should_be_thrown(self, category, user_id):
        with pytest.raises(CommandError) as exc_info:
            call_command('seed_playbook_assignments', category_id=category.id, user_id=user_id)

        assert str(exc_info.value) == 'The --user-id argument must be an integer value greater than or equal to 1.'

    def test_when_count_argument_is_not_provided_then_10_assignments_should_be_created(self, category, regular_user):
        call_command('seed_playbook_assignments')

        assert PlaybookAssignment.objects.count() == 10

    @pytest.mark.parametrize('count', [-10, 0, 0.5, 'invalid'])
    def test_when_count_argument_is_invalid_then_error_should_be_thrown(self, count):
        with pytest.raises(CommandError) as exc_info:
            call_command('seed_playbook_assignments', count=count)

        assert str(exc_info.value) == 'The --count argument must be an integer value greater than or equal to 1.'

    @pytest.mark.parametrize('count', [1, 5, 12])
    def test_when_count_argument_is_provided_then_requested_number_of_assignments_should_be_created(
            self, category, regular_user, count
    ):
        call_command('seed_playbook_assignments', count=count)

        assert PlaybookAssignment.objects.count() == count

    def test_when_category_is_not_provided_then_one_of_existing_categories_should_be_used(
            self, regular_user, category_factory
    ):
        categories_count = 5
        categories = category_factory.create_batch(categories_count)
        call_command('seed_playbook_assignments')

        existing_category_ids = {category.pk for category in categories}
        used_category_ids = {assignment.category_id for assignment in PlaybookAssignment.objects.all()}

        # Since the category selection is randomized, we can only verify that more than one category was used.
        # There's still a small chance that all 10 assignments receive the same category,
        # but the probability is low enough to be negligible.
        assert len(used_category_ids) > 1

        # Ensure that only existing categories are used and no new categories are created.
        assert used_category_ids - existing_category_ids == set()

    def test_when_category_id_provided_then_all_assignments_should_be_assigned_to_the_same_category(
            self, category, regular_user
    ):
        call_command('seed_playbook_assignments', category_id=category.pk)

        used_category_ids = {assignment.category_id for assignment in PlaybookAssignment.objects.all()}

        assert used_category_ids == {category.pk}

        # Verify that new categories were not created.
        assert Category.objects.count() == 1

    def test_when_user_is_not_provided_then_one_of_existing_users_should_be_used(self, category, regular_user_factory):
        users_count = 5
        users = regular_user_factory.create_batch(users_count)
        call_command('seed_playbook_assignments')

        existing_user_ids = {user.pk for user in users}
        used_user_ids = {assignment.user_id for assignment in PlaybookAssignment.objects.all()}

        # Since the user selection is randomized, we can only verify that more than one user was used.
        # There's still a small chance that all 10 assignments receive the same user,
        # but the probability is low enough to be negligible.
        assert len(used_user_ids) > 1

        # Ensure that only existing users are used and no new categories are created.
        assert used_user_ids - existing_user_ids == set()

    def test_when_user_provided_then_all_assignments_should_be_assigned_to_the_same_user(self, category, regular_user):
        call_command('seed_playbook_assignments', user_id=regular_user.pk)

        used_user_ids = {assignment.user_id for assignment in PlaybookAssignment.objects.all()}

        assert used_user_ids == {regular_user.pk}

        # Verify that new assignment users were not created.
        assert User.objects.count() == 1
