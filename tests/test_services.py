"""Unit tests for the application services."""

from src.core.translator import Translator
from src.services.translation_service import TranslationService


class StubFailingProvider:
    def translate(self, text, source, target):
        raise RuntimeError("provider unavailable")

    def detect_language(self, text):
        return None


def test_translation_service_handles_provider_failures():
    service = TranslationService(
        translator=Translator(provider=StubFailingProvider()),
        storage_service=None,
    )
    result = service.translate("familia", "pt", "kimbundu")
    assert result.is_error
    assert not result.is_success
