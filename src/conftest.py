import pytest
from pytest_factoryboy import register

from users.factories import SiteFactory, UserFactory

# Register user factories
register(UserFactory)
register(SiteFactory)


@pytest.fixture
def client():
    from rest_framework.test import APIClient
    return APIClient()
