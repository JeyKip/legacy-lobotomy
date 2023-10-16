import pytest


@pytest.mark.django_db
def test_admin_user_fixture(admin_user):
    assert admin_user.is_superuser
