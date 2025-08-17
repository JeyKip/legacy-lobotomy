from factory import FactoryError


class FactoryRetryExceededError(FactoryError):
    """
    Raised when a factory reaches the maximum number of attempts
    to create a new object."""
