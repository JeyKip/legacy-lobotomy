import pytest
from pytest_factoryboy import register

from assignments.factories import AssignmentTargetFactory, CategoryFactory
from users.factories import AdminUserFactory, RegularUserFactory, SiteFactory, TeamFactory

# Register user factories
register(AdminUserFactory, 'admin_user')
register(RegularUserFactory, 'regular_user')
register(SiteFactory)
register(TeamFactory)

# Register assignment factories
register(CategoryFactory)
register(AssignmentTargetFactory, 'assignment_target')


@pytest.fixture
def client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def auth_client_factory():
    def auth_client(user):
        from rest_framework.authtoken.models import Token
        from rest_framework.test import APIClient

        Token.objects.get_or_create(user=user)

        return APIClient(HTTP_AUTHORIZATION=f'Token {user.auth_token.key}')

    return auth_client
