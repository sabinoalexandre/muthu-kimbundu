"""Machine translation provider placeholder."""

from typing import Optional

from src.core.exceptions import ProviderError
from src.core.translation_result import TranslationResult
from src.providers.base_provider import TranslationProvider


class MachineTranslationProvider(TranslationProvider):
    """Placeholder for a future machine translation provider.

    No machine translation service has been verified so far to support
    Kimbundu reliably, therefore this provider does not translate yet and
    fails explicitly instead of returning unverified results.
    """

    def translate(self, text: str, source: str, target: str) -> TranslationResult:
        """Machine translation is not available yet."""
        raise ProviderError(
            "No verified Kimbundu machine translation model is integrated "
            "yet. Use the LocalDictionaryProvider or another verified "
            "provider instead."
        )

    def detect_language(self, text: str) -> Optional[str]:
        """Automatic language detection is not available yet."""
        raise ProviderError(
            "Automatic language detection is not available yet."
        )
