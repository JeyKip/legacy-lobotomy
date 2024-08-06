import uuid

import factory

from users.models import Team


class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Team

    name = factory.LazyFunction(lambda: f'Fake Team #{uuid.uuid4().hex}')
    description = factory.Faker('text')
    logo = factory.django.ImageField()
