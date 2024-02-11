import factory
from django.db.models.signals import post_save

from assignments.factories.category import CategoryFactory
from playbooks.models import PlaybookAssignment
from users.factories import UserFactory


# We don't want the calculate_total_points signal handler to be called because it updates a related object of the
# User model which in its turn triggers the assign_to_changed_user signal handler that works really slowly.
# As a drawback of this solution, all users will have total_points field equal to 0.
@factory.django.mute_signals(post_save)
class PlaybookAssignmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PlaybookAssignment

    user = factory.SubFactory(UserFactory)
    name = factory.Faker('sentence')
    description = factory.Faker('paragraph')
    image = factory.django.ImageField()
    points = factory.Faker('pyint', min_value=0, max_value=100)
    time = factory.Faker('pyint', min_value=10, max_value=300)
    category = factory.SubFactory(CategoryFactory)
    priority = factory.Faker('pyint', min_value=0, max_value=25)
