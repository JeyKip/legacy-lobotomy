from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm

from .models import User
from .utils import generate_password, send_password_to_new_user


class UserCreationForm(DjangoUserCreationForm):
    password1 = None
    password2 = None

    def clean(self):
        if User.objects.filter(email=self.cleaned_data.get('email')) \
                or len(self.errors) > 0:
            return super().clean()
        password = generate_password()  # here you want to maybe send a signal which can be picked up or something
        self.cleaned_data['password1'] = password
        self.cleaned_data['password2'] = password
        send_password_to_new_user(self.cleaned_data.get('email'), password)
        return super().clean()
