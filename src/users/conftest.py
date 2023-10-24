from pytest_factoryboy import register

from .factories import UserFactory
from .tests.fixtures import uid  # noqa

register(UserFactory)
