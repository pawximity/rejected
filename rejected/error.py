class RejectedError(Exception):
    """Base exception for expected application errors."""


class ResourceNotFoundError(RejectedError):
    """A requested resource does not exist."""


class ValidationError(RejectedError):
    """Invalid input or business rule violation."""
