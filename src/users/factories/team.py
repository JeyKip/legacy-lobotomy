import factory

from users.models import Team


class TeamFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Team

    name = factory.Sequence(lambda n: f'Legacy Lobotomy Team #{n}')
    description = factory.Faker('text')
    logo = factory.django.ImageField()
