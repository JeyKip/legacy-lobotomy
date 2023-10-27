from pytest_factoryboy import register

from .factories import SiteFactory, UserFactory
from .tests.fixtures import uid  # noqa

register(UserFactory)
register(SiteFactory)
