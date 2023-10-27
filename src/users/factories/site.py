import factory
from django.contrib.sites.models import Site


class SiteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Site

    domain = factory.Faker('domain_name')
    name = factory.Faker('sentence', nb_words=3)
