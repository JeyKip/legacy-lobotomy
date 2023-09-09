from django.conf import settings
from django.core.mail import send_mail
from strgen import StringGenerator as SG


def generate_password():
    password = SG(r'[\u]{2}&[\c]{2}&[\d]{2}&[\p]{2}').render()
    print(password)
    return password


def send_password_to_new_user(email, password):
    subject = 'Legacy Lobotomy User Password'
    message = f'Hi {email}, Your password is: {password}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, message, email_from, recipient_list)
