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
    def test_get_users_method_should_return_404_not_found_error(self, user, auth_client_factory):
        auth_client = auth_client_factory(user)
        response = auth_client.get('/api/users/')

        assert response.status_code == status.HTTP_404_NOT_FOUND

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
        update_data = {**self.update_user_payload(another_user), 'is_superuser': True}

        auth_client = auth_client_factory(user)
        response = auth_client.put(f'/api/users/{another_user.pk}/', update_data)

        another_user.refresh_from_db()

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert another_user.is_superuser is False

    @pytest.mark.django_db
    def test_patch_request_should_not_be_allowed(self, user, auth_client_factory):
        auth_client = auth_client_factory(user)
        response = auth_client.patch(f'/api/users/{user.pk}/', {'first_name': 'John'})

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_authenticated_user_cannot_delete_another_user(self, user, user_factory, auth_client_factory):
        another_user = user_factory()

        auth_client = auth_client_factory(user)
        response = auth_client.delete(f'/api/users/{another_user.pk}/')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert User.objects.filter(pk=another_user.pk).exists() is True
