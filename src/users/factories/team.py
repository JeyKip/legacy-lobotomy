import uuid

import factory

from libs.factory.django import RetryableDjangoModelFactory
from users.factories.providers import TeamProvider
from users.models import Team

# Register the custom provider
factory.Faker.add_provider(TeamProvider)


class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Team

    name = factory.LazyFunction(lambda: f'Fake Team #{uuid.uuid4().hex}')
    description = factory.Faker('text')
    logo = factory.django.ImageField()


class RealisticTeamFactory(RetryableDjangoModelFactory, TeamFactory):
    class Meta:
        model = Team

    name = factory.Faker('team_name')
