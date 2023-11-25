import factory
import faker
from django.contrib.auth import get_user_model

fake = faker.Faker()
User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f'fake-user-{n}@fakemail.com')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    age = factory.Faker('pyint', min_value=13, max_value=99)
    gender = factory.Faker('random_element', elements=[item[0] for item in User.GENDER_CHOICES])
    guardian_email = factory.Faker('email')
    accepted_terms_cond = factory.Faker('pybool')
    activity = factory.Faker('random_element', elements=[item[0] for item in User.ACTIVITY_CHOICES])
    total_points = factory.Faker('pyint')
    first_login = factory.Faker('pybool')
    is_superuser = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        user = super()._create(model_class, *args, **kwargs)
        user.set_password(user.password)
        user.save()

        return user
