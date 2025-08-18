import uuid

import factory
import faker
from django.contrib.auth import get_user_model
from faker.utils.text import slugify

from libs.factory.django import RetryableDjangoModelFactory
from .team import RealisticTeamFactory, TeamFactory

fake = faker.Faker()
User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.LazyFunction(lambda: f'fake-user-{uuid.uuid4().hex}@fakemail.com')
    password = factory.django.Password('123456')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    age = factory.Faker('pyint', min_value=13, max_value=99)
    gender = factory.Faker('random_element', elements=[item[0] for item in User.GENDER_CHOICES])
    guardian_email = factory.Faker('email')
    accepted_terms_cond = factory.Faker('pybool')
    activity = factory.Faker('random_element', elements=[item[0] for item in User.ACTIVITY_CHOICES])
    total_points = factory.Faker('pyint')
    first_login = factory.Faker('pybool')


class AdminUserFactory(UserFactory):
    is_superuser = True
    is_staff = True


class RegularUserFactory(UserFactory):
    is_superuser = False
    is_staff = False
    team = factory.SubFactory(TeamFactory)


class RealisticRegularUserFactory(RetryableDjangoModelFactory, RegularUserFactory):
    class Meta:
        model = User

    team = factory.SubFactory(RealisticTeamFactory)

    @factory.lazy_attribute
    def email(self):
        first_name = slugify(self.first_name)
        last_name = slugify(self.last_name)
        team_name = slugify(self.team.name)

        return f'{first_name}.{last_name}@{team_name}.{fake.tld()}'
