import factory
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f'fake-user-{n}@fakemail.com')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        user = super()._create(model_class, *args, **kwargs)
        user.set_password(user.password)
        user.save()

        return user
