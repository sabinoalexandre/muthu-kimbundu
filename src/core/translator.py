"""Translation orchestration business logic."""

from typing import Optional

from src.core.exceptions import ProviderError, UnsupportedTranslationError
from src.core.translation_result import TranslationResult


class Translator:
    """Orchestrates translation requests through a pluggable provider."""

    def __init__(self, provider) -> None:
        self.provider = provider

    @property
    def provider_name(self) -> str:
        """Return the provider implementation name."""
        return type(self.provider).__name__

    def detect_language(self, text: str) -> Optional[str]:
        """Detect the language of ``text`` when the provider supports it."""
        return self.provider.detect_language(text)

    def translate(self, text: str, source: str, target: str) -> TranslationResult:
        """Translate ``text`` from ``source`` into ``target``."""
        from src.core.validators import validate_translation_request

        stripped = (text or "").strip()
        error = validate_translation_request(stripped, source or "", target or "")
        if error is not None:
            return TranslationResult.error(
                stripped,
                source or "",
                target or "",
                error,
                method=self.provider_name,
            )

        try:
            result = self.provider.translate(stripped, source, target)
        except UnsupportedTranslationError as exc:
            return TranslationResult.unsupported(stripped, source, target, str(exc))
        except ProviderError as exc:
            return TranslationResult.error(
                stripped, source, target, str(exc), method=self.provider_name
            )

        result.source_language = source
        result.target_language = target
        result.original_text = stripped
        return result
