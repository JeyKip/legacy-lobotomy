import pytest
from rest_framework import status


class TestLogin:
    login_endpoint = '/auth/login/'

    @pytest.mark.parametrize('body, expected_error', [
        pytest.param({}, 'This field is required.', id='request body is empty'),
        pytest.param({'email': 'fake-user-email@fake.com'}, 'This field is required.', id='password is missing'),
        pytest.param({'password': ''}, 'This field may not be blank.', id='email is missing, password is blank'),
        pytest.param(
            {'email': 'fake-user-email@fake.com', 'password': ''},
            'This field may not be blank.',
            id='password is blank'
        ),
    ])
    def test_when_password_is_missing_or_invalid_then_400_bad_request_status_should_be_returned(
            self, body, expected_error, client
    ):
        response = client.post(self.login_endpoint, body)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            'password': [expected_error]
        }

    @pytest.mark.django_db
    @pytest.mark.parametrize('body', [
        pytest.param({'password': '123456'}, id='email field is missing'),
        pytest.param({'password': '123456', 'email': ''}, id='email field is blank'),
        pytest.param({'password': '123456', 'email': 'fake-user-email@fake.com'}, id='user with email does not exist'),
    ])
    def test_when_email_field_is_missing_and_password_valid_then_400_bad_request_status_should_be_returned(
            self, body, client
    ):
        response = client.post(self.login_endpoint, body)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'non_field_errors': ['Unable to log in with provided credentials.']}

    @pytest.mark.django_db
    @pytest.mark.parametrize('user_email, user_password, login_email, login_password', [
        pytest.param('user-1@fake.com', 'user-1-pass', 'user-1@fake.com', 'invalid-password', id='invalid password'),
        pytest.param('user-2@fake.com', 'user-2-pass', 'invalid-email@fake.com', 'user-2-pass', id='invalid email'),
        pytest.param(
            'user-3@fake.com', 'user-3-pass', 'user-3@fake.com', ' user-3-pass', id='password starts with a whitespace'
        ),
        pytest.param(
            'user-4@fake.com', 'user-4-pass', 'user-4@fake.com', 'user-4-pass ', id='password ends with a whitespace'
        ),
    ])
    def test_when_credentials_are_invalid_then_400_bad_request_status_should_be_returned(
            self, user_email, user_password, login_email, login_password, user_factory, client
    ):
        user_factory(email=user_email, password=user_password)
        response = client.post(self.login_endpoint, {'email': login_email, 'password': login_password})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            'non_field_errors': ['Unable to log in with provided credentials.']
        }

    @pytest.mark.django_db
    def test_when_credentials_are_valid_then_token_and_user_details_should_be_returned(
            self, faker, user_factory, client
    ):
        password = faker.pystr()
        user = user_factory(password=password)

        response = client.post(self.login_endpoint, {'email': user.email, 'password': password})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            'key': user.auth_token.key,
            'user': {
                'pk': user.pk,
                'email': user.email,
                'first_login': user.first_login,
                'accepted_terms_cond': user.accepted_terms_cond,
            }
        }
