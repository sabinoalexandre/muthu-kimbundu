"""Translation provider abstraction."""

from abc import ABC, abstractmethod
from typing import Optional

from src.core.translation_result import TranslationResult


class TranslationProvider(ABC):
    """Interface implemented by translation providers."""

    @abstractmethod
    def translate(self, text: str, source: str, target: str) -> TranslationResult:
        """Translate ``text`` from ``source`` language into ``target``.

        Implementations must return a :class:`TranslationResult` and must
        never present uncertain translations as confirmed ones.

        Raises:
            src.core.exceptions.ProviderError: when the provider fails.
            src.core.exceptions.UnsupportedTranslationError: when no reliable
                translation is available for the input.
        """
        raise NotImplementedError

    @abstractmethod
    def detect_language(self, text: str) -> Optional[str]:
        """Detect the language of ``text``.

        Returns:
            The detected language code, or ``None`` when detection is not
            reliable.
        """
        raise NotImplementedError
