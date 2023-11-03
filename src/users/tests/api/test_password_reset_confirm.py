import random

# 1. It provides a convenient way to get access to groups of symbols
import string

import pytest
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status


class TestPasswordResetConfirm:
    # 2. Define an endpoint which should handle requests for changing the password
    reset_password_confirm_endpoint = '/auth/password/reset/confirm/'

    # 3. Define a password that's guaranteed to be valid
    valid_password = 'Super#StrongPassword123'

    # 4. Define a password that will be valid if add a digit
    password_without_digit = 'StrongPassword?'

    # 5. Define a password that will be valid if add an uppercase letter
    password_without_uppercase_letter = 'password1?'

    # 6. Define a password that will be valid if add a lowercase letter
    password_without_lowercase_letter = 'PASSWORD1?'

    # 7. Define a password that will be valid if add a special symbol
    password_without_special_symbol = 'StrongPassword1'

    # 8. A list of possible locations of the symbol in the string
    symbol_positions = ['beginning', 'middle', 'ending']

    # 9. Define a fixture with a valid body for changing the password of the user passed as an argument
    @pytest.fixture
    def valid_request_body(self, user, uid):
        return {
            'new_password1': self.valid_password,
            'new_password2': self.valid_password,
            'uid': uid(user.pk),
            'token': default_token_generator.make_token(user),
        }

    # 10. A helper method which inserts a tested symbol into the tested password value
    def _insert_symbol_into_string(self, destination, symbol, position):
        if position == 'beginning':
            return f'{symbol}{destination}'
        if position == 'ending':
            return f'{destination}{symbol}'

        index = random.randint(1, len(destination) - 1)

        return f'{destination[:index]}{symbol}{destination[index:]}'

    def test_when_request_body_is_empty_then_400_bad_request_status_should_be_returned(self, client):
        response = client.post(self.reset_password_confirm_endpoint, {})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            'new_password1': ['This field is required.'],
            'new_password2': ['This field is required.'],
            'uid': ['This field is required.'],
            'token': ['This field is required.']
        }

    @pytest.mark.django_db
    @pytest.mark.parametrize('missed_field_name', [
        pytest.param('new_password1', id='new_password1 is not present'),
        pytest.param('new_password2', id='new_password2 is not present'),
        pytest.param('uid', id='uid is not present'),
        pytest.param('token', id='token is not present'),
    ])
    def test_when_a_single_required_field_is_missing_then_400_bad_request_status_should_be_returned(
            self, valid_request_body, missed_field_name, client
    ):
        request_body = {**valid_request_body}
        request_body.pop(missed_field_name, None)
        response = client.post(self.reset_password_confirm_endpoint, request_body)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            missed_field_name: ['This field is required.'],
        }

    @pytest.mark.django_db
    @pytest.mark.parametrize(
        'field_name, value, expected_message', [
            pytest.param('new_password1', '', 'This field may not be blank.', id='new_password1 is empty'),
            pytest.param(
                'new_password1', 'a' * 129,
                'Ensure this field has no more than 128 characters.',
                id='new_password1 consists of 129 symbols'
            ),
            pytest.param('new_password2', '', 'This field may not be blank.', id='new_password2 is empty'),
            pytest.param(
                'new_password2', 'a' * 129,
                'Ensure this field has no more than 128 characters.',
                id='new_password2 consists of 129 symbols'
            ),
            pytest.param('uid', '', 'This field may not be blank.', id='uid is empty'),
            pytest.param('uid', 'invalid_uid_value', 'Invalid value', id='uid is invalid'),
            pytest.param('token', '', 'This field may not be blank.', id='token is empty'),
            pytest.param('token', 'invalid_token_value', 'Invalid value', id='token is invalid'),
        ]
    )
    def test_when_at_least_one_field_is_invalid_then_400_bad_request_status_should_be_returned(
            self, field_name, value, expected_message, valid_request_body, client
    ):
        request_body = {**valid_request_body, field_name: value}
        response = client.post(self.reset_password_confirm_endpoint, request_body)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {field_name: [expected_message]}

    @pytest.mark.django_db
    @pytest.mark.parametrize('password, expected_message', [
        pytest.param(
            'Short#1', 'This password is too short. It must contain at least 8 characters.', id='short password'
        ),
        pytest.param('12345678', 'This password is too common.', id='common password'),
        pytest.param(
            password_without_digit,
            'The password must contain at least 1 digit, 0-9.',
            id='password without digit'
        ),
        pytest.param(
            password_without_uppercase_letter,
            'The password must contain at least 1 uppercase letter, A-Z.',
            id='password without uppercase letter'
        ),
        pytest.param(
            password_without_lowercase_letter,
            'The password must contain at least 1 lowercase letter, a-z.',
            id='password without lowercase letter'
        ),
        pytest.param(
            password_without_special_symbol,
            f'The password must contain at least 1 symbol: {string.punctuation}',
            id='password without special symbol'
        ),
        pytest.param(
            ' StrongPassword1?',
            'The password must not contain any space character.',
            id='password with a space at the beginning'
        ),
        pytest.param(
            'StrongPassword1? ',
            'The password must not contain any space character.',
            id='password with a space at the end'
        ),
        pytest.param(
            'Strong Password1?',
            'The password must not contain any space character.',
            id='password with a space in the middle'
        ),
    ])
    def test_when_password_is_not_strong_enough_then_400_bad_request_status_should_be_returned(
            self, password, expected_message, valid_request_body, client
    ):
        request_body = {**valid_request_body, 'new_password1': password, 'new_password2': password}
        response = client.post(self.reset_password_confirm_endpoint, request_body)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_message in response.json()['new_password2']

    @pytest.mark.django_db
    @pytest.mark.parametrize('field_name, value', [
        ('new_password1', ' ' + valid_password),
        ('new_password1', valid_password + ' '),
        ('new_password2', ' ' + valid_password),
        ('new_password2', valid_password + ' '),
    ])
    def test_when_password_field_has_extra_leading_or_trailing_space_then_passwords_should_not_match(
            self, field_name, value, valid_request_body, client
    ):
        request_body = {**valid_request_body, field_name: value}
        response = client.post(self.reset_password_confirm_endpoint, request_body)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'new_password2': ['The two password fields didn’t match.']}

    @pytest.mark.django_db
    @pytest.mark.parametrize('symbol_position', symbol_positions)
    @pytest.mark.parametrize('symbol', list(string.digits))
    def test_when_password_has_digit_at_any_position_it_should_be_saved(
            self, symbol_position, symbol, user, valid_request_body, client
    ):
        password = self._insert_symbol_into_string(self.password_without_digit, symbol, symbol_position)
        request_body = {**valid_request_body, 'new_password1': password, 'new_password2': password}
        response = client.post(self.reset_password_confirm_endpoint, request_body)

        user.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert user.check_password(password)

    @pytest.mark.django_db
    @pytest.mark.parametrize('symbol_position', symbol_positions)
    @pytest.mark.parametrize('symbol', list(string.ascii_lowercase))
    def test_when_password_has_lowercase_letter_at_any_position_it_should_be_saved(
            self, symbol_position, symbol, user, valid_request_body, client
    ):
        password = self._insert_symbol_into_string(self.password_without_lowercase_letter, symbol, symbol_position)
        request_body = {**valid_request_body, 'new_password1': password, 'new_password2': password}
        response = client.post(self.reset_password_confirm_endpoint, request_body)

        user.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert user.check_password(password)

    @pytest.mark.django_db
    @pytest.mark.parametrize('symbol_position', symbol_positions)
    @pytest.mark.parametrize('symbol', list(string.ascii_uppercase))
    def test_when_password_has_uppercase_letter_at_any_position_it_should_be_saved(
            self, symbol_position, symbol, user, valid_request_body, client
    ):
        password = self._insert_symbol_into_string(self.password_without_uppercase_letter, symbol, symbol_position)
        request_body = {**valid_request_body, 'new_password1': password, 'new_password2': password}
        response = client.post(self.reset_password_confirm_endpoint, request_body)

        user.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert user.check_password(password)

    @pytest.mark.django_db
    @pytest.mark.parametrize('symbol_position', symbol_positions)
    @pytest.mark.parametrize('symbol', list(string.punctuation))
    def test_when_password_has_special_symbol_at_any_position_it_should_be_saved(
            self, symbol_position, symbol, user, valid_request_body, client
    ):
        password = self._insert_symbol_into_string(self.password_without_special_symbol, symbol, symbol_position)
        request_body = {**valid_request_body, 'new_password1': password, 'new_password2': password}
        response = client.post(self.reset_password_confirm_endpoint, request_body)

        user.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert user.check_password(password)
