from unittest.mock import patch

import pytest
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status


class TestPasswordReset:
    reset_password_endpoint = '/auth/password/reset/'

    def test_when_email_field_is_absent_then_400_bad_request_status_should_be_returned(self, client):
        body = {}
        response = client.post(self.reset_password_endpoint, body)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'email': ['This field is required.']}

    @pytest.mark.parametrize(
        'email, expected_message',
        [
            ('', 'This field may not be blank.'),
            ('invalid-email', 'Enter a valid email address.'),
            ('invalid-email@', 'Enter a valid email address.'),
            ('invalid-email@fake', 'Enter a valid email address.'),
            (
                    'email' + 'a' * (255 - len('email@fake.com')) + '@fake.com',
                    "Ensure this value has at most 254 characters (it has 255)."
            )
        ]
    )
    def test_when_request_has_invalid_data_then_400_bad_request_status_should_be_returned(
            self, email, expected_message, client
    ):
        response = client.post(self.reset_password_endpoint, {'email': email})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'email': [expected_message]}

    @pytest.mark.django_db
    def test_when_user_with_specified_email_does_not_exist_then_email_should_not_be_sent(
            self, faker, client, mailoutbox
    ):
        response = client.post(self.reset_password_endpoint, {'email': faker.email()})

        assert response.status_code == status.HTTP_200_OK
        assert len(mailoutbox) == 0

    @pytest.mark.django_db
    @patch.object(default_token_generator, 'make_token')
    def test_when_user_with_specified_email_exists_then_password_reset_email_should_be_sent(
            self, make_token_mock, faker, uid, user, client, mailoutbox
    ):
        password_reset_token = faker.pystr()
        make_token_mock.return_value = password_reset_token

        response = client.post(self.reset_password_endpoint, {'email': user.email})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {'detail': 'Password reset e-mail has been sent.'}

        [email] = mailoutbox
        [alternative_content, alternative_type] = email.alternatives[0]

        assert email.subject == 'Password reset on Legacy Lobotomy'
        assert email.to == [user.email]

        assert email.body.strip() == f'''
You're receiving this email because you requested a password reset for your user account at example.com.

Please go to the following page and choose a new password:

http://example.com/auth/password-reset-confirm/{uid(user.pk)}/{password_reset_token}/

Your username, in case you’ve forgotten: {user.email}

Thanks for using our site!

The example.com team
'''.strip()

        assert alternative_content.strip() == f'''
You're receiving this email because you requested a password reset for your user account.
<br>
Please click on the following link and choose a new password:
<br>
<a href="https://legacy-Lobotomy-be.com/password-reset-confirm/{uid(user.pk)}/{password_reset_token}/">https://legacy-lobotomy-be.com/password-reset-confirm/{uid(user.pk)}/{password_reset_token}/</a>
<br>
Your email, in case you’ve forgotten: {user.email}
<br>
Thanks for using our site!
        '''.strip()
        assert alternative_type == 'text/html'
