import pytest
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


@pytest.fixture
def uid():
    def uid_internal(value):
        return urlsafe_base64_encode(force_bytes(value))

    return uid_internal
