import factory
from django.db import IntegrityError, transaction

from .exceptions import FactoryRetryExceededError


class RetryableDjangoOptions(factory.django.DjangoOptions):
    """
    Extends the default DjangoOptions to add a `max_retry_attempts`
    setting for factories.

    This option defines how many times a factory should retry
    creating an object when database integrity errors (such as
    unique constraint violations) occur.

    It is inherited by subclasses, so the retry behavior is
    consistent across all factories that use this option class.

    Attributes:
        max_retry_attempts (int): The maximum number of creation
            attempts before giving up and raising an error.
            Defaults to 300.
    """

    def _build_default_options(self):
        return super()._build_default_options() + [
            factory.base.OptionDefault('max_retry_attempts', 300, inherit=True),
        ]


class RetryableDjangoModelFactory(factory.django.DjangoModelFactory):
    """
    A DjangoModelFactory that will retry creating a new object
    if IntegrityError is raised.
    """

    _options_class = RetryableDjangoOptions

    class Meta:
        abstract = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        for _ in range(cls._meta.max_retry_attempts):
            try:
                # Without this atomic() scoping, once we hit an
                # IntegrityError on the first insert, the transaction
                # is permanently marked dead for the duration of the
                # test or request, and every subsequent query will
                # immediately fail with TransactionManagementError.
                # The nested atomic() is the only way to recover
                # cleanly, roll back just the failed insert, and keep
                # retry logic running. For more details, check out
                # the official Django documentation:
                # https://docs.djangoproject.com/en/3.2/topics/db/transactions/#controlling-transactions-explicitly
                with transaction.atomic():
                    return super()._create(model_class, *args, **kwargs)
            except IntegrityError:
                # If an IntegrityError occurs, we catch it and retry
                # until we've exhausted the maximum number of attempts.
                pass

        # If we exhaust our retries, raise an error.
        raise FactoryRetryExceededError(
            f"Failed to create {model_class.__name__} after {cls._meta.max_retry_attempts} attempts "
            f"due to repeated IntegrityError."
        )
