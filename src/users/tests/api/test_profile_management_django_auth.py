import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

from users.factories import AdminUserFactory, RegularUserFactory

User = get_user_model()


class TestProfileManagementDjangoAuth:
    profile_endpoint = '/auth/user/'

    def update_user_payload(self, user):
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'age': user.age,
            'gender': user.gender,
            'guardian_email': user.guardian_email,
            'activity': user.activity,
        }

    @pytest.mark.django_db
    def test_patch_request_should_not_be_allowed(self, regular_user, auth_client_factory):
        auth_client = auth_client_factory(regular_user)
        response = auth_client.patch(self.profile_endpoint, {'first_name': 'John'})

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    @pytest.mark.django_db
    @pytest.mark.parametrize('method', ['get', 'put', 'delete'])
    def test_when_user_is_not_authenticated_then_401_unauthorized_code_should_be_returned(
            self, method, regular_user, client
    ):
        method_callable = getattr(client, method)
        response = method_callable(self.profile_endpoint)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    @pytest.mark.parametrize('user_factory', [
        pytest.param(AdminUserFactory, id='user is a superuser'),
        pytest.param(RegularUserFactory, id='user is a regular user'),
    ])
    def test_get_method_with_authenticated_user(self, user_factory, auth_client_factory):
        user = user_factory()
        auth_client = auth_client_factory(user)
        response = auth_client.get(self.profile_endpoint)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            'pk': user.pk,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'age': user.age,
            'gender': user.gender,
            'guardian_email': user.guardian_email,
            'accepted_terms_cond': user.accepted_terms_cond,
            'activity': user.activity,
            'total_points': user.total_points,
            'first_login': user.first_login,
            'is_superuser': user.is_superuser,
        }

    @pytest.mark.django_db
    def test_put_method_should_return_403_forbidden_when_user_is_a_superuser(self, admin_user, auth_client_factory):
        auth_client = auth_client_factory(admin_user)
        response = auth_client.put(self.profile_endpoint, self.update_user_payload(admin_user))

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_put_method_should_return_200_ok_when_user_is_a_regular_user(self, regular_user, auth_client_factory):
        auth_client = auth_client_factory(regular_user)
        response = auth_client.put(self.profile_endpoint, self.update_user_payload(regular_user))

        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_delete_method_should_return_403_forbidden_when_user_is_a_superuser(self, admin_user, auth_client_factory):
        auth_client = auth_client_factory(admin_user)
        response = auth_client.delete(self.profile_endpoint)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_delete_method_should_return_204_no_content_when_user_is_a_regular_user(
            self, regular_user, auth_client_factory
    ):
        auth_client = auth_client_factory(regular_user)
        response = auth_client.delete(self.profile_endpoint)

        assert response.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.django_db
    @pytest.mark.parametrize('updated_first_login', [
        pytest.param(True, id='updated_first_login = True'),
        pytest.param(False, id='updated_first_login = False'),
    ])
    @pytest.mark.parametrize('regular_user__first_login', [
        pytest.param(True, id='regular_user__first_login = True'),
        pytest.param(False, id='regular_user__first_login = False'),
    ])
    def test_put_method_first_login_value_should_become_false_regardless_of_the_request_value(
            self, regular_user, auth_client_factory, updated_first_login
    ):
        payload = {**self.update_user_payload(regular_user), 'first_login': updated_first_login}

        auth_client = auth_client_factory(regular_user)
        auth_client.put(self.profile_endpoint, payload)

        regular_user.refresh_from_db()

        assert regular_user.first_login is False

    @pytest.mark.django_db
    @pytest.mark.parametrize('regular_user__first_login', [
        pytest.param(True, id='regular_user__first_login = True'),
        pytest.param(False, id='regular_user__first_login = False'),
    ])
    def test_put_method_first_login_value_should_become_false_even_if_request_does_not_contain_first_login_field(
            self, regular_user, auth_client_factory
    ):
        payload = self.update_user_payload(regular_user)

        auth_client = auth_client_factory(regular_user)
        auth_client.put(self.profile_endpoint, payload)

        regular_user.refresh_from_db()

        assert regular_user.first_login is False

    @pytest.mark.django_db
    @pytest.mark.parametrize('field_name, current_value, new_value', [
        pytest.param('id', 100, 200, id='id: 100 -> 200'),
        pytest.param('email', 'fake-user.old-email@fake.com', 'fake-user.new-email@fake.com', id='email'),
        pytest.param('accepted_terms_cond', False, True, id='accepted_terms_cond: False -> True'),
        pytest.param('accepted_terms_cond', True, False, id='accepted_terms_cond: True -> False'),
        pytest.param('total_points', 0, 100, id='total_points'),
        pytest.param('is_superuser', False, True, id='is_superuser: False -> True'),
        pytest.param('is_superuser', True, False, id='is_superuser: True -> False'),
    ])
    def test_put_method_readonly_fields_should_not_be_updated(
            self, field_name, current_value, new_value, regular_user_factory, auth_client_factory
    ):
        user = regular_user_factory(**{field_name: current_value})
        payload = {**self.update_user_payload(user), field_name: new_value}

        auth_client = auth_client_factory(user)
        auth_client.put(self.profile_endpoint, payload)

        user.refresh_from_db()

        assert getattr(user, field_name) == current_value

    @pytest.mark.django_db
    @pytest.mark.parametrize('field_name', [
        'first_name', 'last_name', 'gender', 'guardian_email', 'age', 'activity'
    ])
    def test_put_method_when_required_field_is_not_passed_then_400_bad_request_status_should_be_returned(
            self, field_name, regular_user, auth_client_factory
    ):
        payload = self.update_user_payload(regular_user)
        payload.pop(field_name)

        auth_client = auth_client_factory(regular_user)
        response = auth_client.put(self.profile_endpoint, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {field_name: ['This field is required.']}

    @pytest.mark.django_db
    @pytest.mark.parametrize('field_name, value, expected_error', [
        pytest.param('first_name', None, 'This field may not be null.', id='first_name is null'),
        pytest.param('first_name', '', 'This field may not be blank.', id='first_name is empty'),
        pytest.param('first_name', '   ', 'This field may not be blank.', id='first_name is blank'),
        pytest.param(
            'first_name',
            'a' * 151, 'Ensure this field has no more than 150 characters.',
            id='first_name is too long'
        ),
        pytest.param('last_name', None, 'This field may not be null.', id='last_name is null'),
        pytest.param('last_name', '', 'This field may not be blank.', id='last_name is empty'),
        pytest.param('last_name', '   ', 'This field may not be blank.', id='last_name is blank'),
        pytest.param(
            'last_name',
            'a' * 151, 'Ensure this field has no more than 150 characters.',
            id='last_name is too long'
        ),
        pytest.param('gender', None, 'This field may not be null.', id='gender is null'),
        pytest.param('gender', '', '"" is not a valid choice.', id='gender is empty'),
        pytest.param('gender', '   ', '"   " is not a valid choice.', id='gender is blank'),
        pytest.param('gender', 'invalid', '"invalid" is not a valid choice.', id='gender value is not allowed'),
        pytest.param('guardian_email', None, 'This field may not be null.', id='guardian_email is null'),
        pytest.param('guardian_email', '', 'This field may not be blank.', id='guardian_email is empty'),
        pytest.param('guardian_email', '   ', 'This field may not be blank.', id='guardian_email is blank'),
        pytest.param(
            'guardian_email', 'invalid-email', 'Enter a valid email address.', id='guardian_email is invalid 1'
        ),
        pytest.param(
            'guardian_email', 'invalid-email@', 'Enter a valid email address.', id='guardian_email is invalid 2'
        ),
        pytest.param(
            'guardian_email', 'invalid-email@fake', 'Enter a valid email address.', id='guardian_email is invalid 3'
        ),
        pytest.param(
            'guardian_email',
            'email' + 'a' * (255 - len('email@fake.com')) + '@fake.com',
            'Ensure this field has no more than 254 characters.',
            id='guardian_email is too long',
        ),
        pytest.param('age', None, 'This field may not be null.', id='age is null'),
        pytest.param('age', '', 'A valid integer is required.', id='age is empty'),
        pytest.param('age', '   ', 'A valid integer is required.', id='age is blank'),
        pytest.param('age', 12, 'Ensure this value is greater than or equal to 13.', id='age is below minimum allowed'),
        pytest.param('age', 100, 'Ensure this value is less than or equal to 99.', id='age exceeds maximum allowed'),
        pytest.param('age', 45.28, 'A valid integer is required.', id='age is not an integer'),
        pytest.param('activity', None, 'This field may not be null.', id='activity is null'),
        pytest.param('activity', '', '"" is not a valid choice.', id='activity is empty'),
        pytest.param('activity', '   ', '"   " is not a valid choice.', id='activity is blank'),
        pytest.param('activity', 'invalid', '"invalid" is not a valid choice.', id='activity value is not allowed'),
    ])
    def test_put_method_when_invalid_value_passed_then_400_bad_request_status_should_be_returned(
            self, field_name, value, expected_error, regular_user, auth_client_factory
    ):
        payload = {**self.update_user_payload(regular_user), field_name: value}

        auth_client = auth_client_factory(regular_user)
        response = auth_client.put(self.profile_endpoint, payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {field_name: [expected_error]}

    @pytest.mark.django_db
    @pytest.mark.parametrize('field_name, current_value, new_value', [
        pytest.param('first_name', 'John', 'Jack'),
        pytest.param('last_name', 'Dou', 'Carter'),
        pytest.param('gender', 'Male', 'Female'),
        pytest.param('guardian_email', 'guardian-fake-email-old@fake.com', 'guardian-fake-email-new@fake.com'),
        pytest.param('age', 99, 13),  # edge case
        pytest.param('age', 25, 45),  # any normal value in the allowed range
        pytest.param('age', 13, 99),  # edge case
        pytest.param('activity', None, 'Law Explorers'),
    ])
    def test_put_method_when_valid_data_passed_then_user_data_should_be_updated(
            self, field_name, current_value, new_value, regular_user_factory, auth_client_factory
    ):
        user = regular_user_factory(**{field_name: current_value})
        payload = {**self.update_user_payload(user), field_name: new_value}

        auth_client = auth_client_factory(user)
        response = auth_client.put(self.profile_endpoint, payload)

        user.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK

        # verify that both response and user entry have a new value of the field
        assert response.json()[field_name] == new_value
        assert getattr(user, field_name) == new_value
