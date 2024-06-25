import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


class TestProfileManagement:
    def user_details_url(self, user):
        return f'/api/users/{user.pk}/'

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
    def test_get_users_method_should_return_only_current_user_details(self, user, user_factory, auth_client_factory):
        another_user = user_factory()
        auth_client = auth_client_factory(user)

        response = auth_client.get('/api/users/')
        returned_users = {item['pk'] for item in response.json()}

        assert response.status_code == status.HTTP_200_OK
        assert returned_users == {user.pk}

    @pytest.mark.django_db
    def test_authenticated_user_cannot_see_details_of_any_other_user_in_the_system(
            self, user, user_factory, auth_client_factory
    ):
        another_user = user_factory()

        auth_client = auth_client_factory(user)
        response = auth_client.get(f'/api/users/{another_user.pk}/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_authenticated_user_cannot_make_another_user_a_superuser(self, user, user_factory, auth_client_factory):
        # first_login=False is used to work around a bug with attempt to change request data
        another_user = user_factory(is_superuser=False, first_login=False)

        auth_client = auth_client_factory(user)
        response = auth_client.patch(f'/api/users/{another_user.pk}/', {'is_superuser': True})

        another_user.refresh_from_db()

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert another_user.is_superuser is False

    @pytest.mark.django_db
    def test_authenticated_user_cannot_delete_another_user(self, user, user_factory, auth_client_factory):
        another_user = user_factory()

        auth_client = auth_client_factory(user)
        response = auth_client.delete(f'/api/users/{another_user.pk}/')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert User.objects.filter(pk=another_user.pk).exists() is True

    @pytest.mark.django_db
    @pytest.mark.parametrize('method', ['get', 'put', 'delete'])
    def test_when_user_is_not_authenticated_then_401_unauthorized_code_should_be_returned(self, method, user, client):
        method_callable = getattr(client, method)
        response = method_callable(self.user_details_url(user))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    @pytest.mark.parametrize('user__is_superuser', [
        pytest.param(True, id='user is a superuser'),
        pytest.param(False, id='user is an regular user'),
    ])
    def test_get_method_with_authenticated_user(self, user, auth_client_factory):
        auth_client = auth_client_factory(user)
        response = auth_client.get(self.user_details_url(user))

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
    @pytest.mark.parametrize('user__is_superuser, expected_status', [
        pytest.param(True, status.HTTP_403_FORBIDDEN, id='a superuser should not be able to update the profile'),
        pytest.param(False, status.HTTP_200_OK, id='a regular user should be able to update the profile'),
    ])
    def test_put_method_with_authenticated_user(self, expected_status, user, auth_client_factory):
        auth_client = auth_client_factory(user)
        response = auth_client.put(self.user_details_url(user), self.update_user_payload(user))

        assert response.status_code == expected_status

    @pytest.mark.django_db
    @pytest.mark.parametrize('user__is_superuser, expected_status', [
        pytest.param(True, status.HTTP_403_FORBIDDEN, id='a superuser should not be able to delete the profile'),
        pytest.param(False, status.HTTP_204_NO_CONTENT, id='a regular user should be able to delete the profile'),
    ])
    def test_delete_method_with_authenticated_user(self, expected_status, user, auth_client_factory):
        auth_client = auth_client_factory(user)
        response = auth_client.delete(self.user_details_url(user))

        assert response.status_code == expected_status

    @pytest.mark.django_db
    @pytest.mark.parametrize('updated_first_login', [
        pytest.param(True, id='updated_first_login = True'),
        pytest.param(False, id='updated_first_login = False'),
    ])
    @pytest.mark.parametrize('user__first_login', [
        pytest.param(True, id='user__first_login = True'),
        pytest.param(False, id='user__first_login = False'),
    ])
    def test_put_method_first_login_value_should_become_false_regardless_of_the_request_value(
            self, user, auth_client_factory, updated_first_login
    ):
        payload = {**self.update_user_payload(user), 'first_login': updated_first_login}

        auth_client = auth_client_factory(user)
        auth_client.put(self.user_details_url(user), payload)

        user.refresh_from_db()

        assert user.first_login is False

    @pytest.mark.django_db
    @pytest.mark.parametrize('user__first_login', [
        pytest.param(True, id='user__first_login = True'),
        pytest.param(False, id='user__first_login = False'),
    ])
    def test_put_method_first_login_value_should_become_false_even_if_request_does_not_contain_first_login_field(
            self, user, auth_client_factory
    ):
        payload = self.update_user_payload(user)

        auth_client = auth_client_factory(user)
        auth_client.put(self.user_details_url(user), payload)

        user.refresh_from_db()

        assert user.first_login is False

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
            self, field_name, current_value, new_value, user_factory, auth_client_factory
    ):
        user = user_factory(**{field_name: current_value})
        payload = {**self.update_user_payload(user), field_name: new_value}

        auth_client = auth_client_factory(user)
        auth_client.put(self.user_details_url(user), payload)

        user.refresh_from_db()

        assert getattr(user, field_name) == current_value
