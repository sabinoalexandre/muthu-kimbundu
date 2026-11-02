"""Domain exceptions used across the MUTHU layers."""

class MuthuError(Exception):
    """Base exception for all MUTHU domain errors."""


class ProviderError(MuthuError):
    """Raised when a translation provider fails or is unavailable."""


class UnsupportedTranslationError(ProviderError):
    """Raised when no reliable translation is available for the input."""
