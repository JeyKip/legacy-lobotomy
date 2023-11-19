import pytest


@pytest.fixture
def client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def auth_client(user, auth_client_factory):
    return auth_client_factory(user)


@pytest.fixture
def auth_client_factory():
    def auth_client(user):
        from rest_framework.authtoken.models import Token
        from rest_framework.test import APIClient

        Token.objects.get_or_create(user=user)

        return APIClient(HTTP_AUTHORIZATION=f'Token {user.auth_token.key}')

    return auth_client
