import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


class TestUsersViewSet:
    @pytest.mark.django_db
    def test_any_authenticated_user_can_see_the_list_of_all_users_in_the_system(self, auth_client, user, user_factory):
        another_user = user_factory()

        response = auth_client.get('/api/users/')
        returned_users = {item['pk'] for item in response.json()}

        assert response.status_code == status.HTTP_200_OK
        assert returned_users == {user.pk, another_user.pk}

    @pytest.mark.django_db
    def test_any_authenticated_user_can_see_details_of_any_user_in_the_system(self, auth_client, user_factory):
        another_user = user_factory()

        response = auth_client.get(f'/api/users/{another_user.pk}/')

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['pk'] == another_user.pk

    @pytest.mark.django_db
    def test_any_authenticated_user_can_make_themselves_a_superuser(self, auth_client_factory, user_factory):
        # first_login=False is used to work around a bug with attempt to change request data
        user = user_factory(is_superuser=False, first_login=False)
        auth_client = auth_client_factory(user)
        response = auth_client.patch(f'/api/users/{user.pk}/', {'is_superuser': True})

        user.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert response.json()['is_superuser']
        assert user.is_superuser

    @pytest.mark.django_db
    def test_any_authenticated_user_can_make_another_user_a_superuser(self, auth_client, user_factory):
        # first_login=False is used to work around a bug with attempt to change request data
        another_user = user_factory(is_superuser=False, first_login=False)
        response = auth_client.patch(f'/api/users/{another_user.pk}/', {'is_superuser': True})

        another_user.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK

        # verify that another user is already superuser
        assert response.json()['is_superuser']
        assert another_user.is_superuser

    @pytest.mark.django_db
    def test_any_authenticated_user_can_delete_another_user(self, auth_client, user_factory):
        another_user = user_factory()

        response = auth_client.delete(f'/api/users/{another_user.pk}/')

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # verify that an attempt to read the entry again causes the User.DoesNotExist exception
        # that means that this user no longer exists
        with pytest.raises(User.DoesNotExist):
            another_user.refresh_from_db()
