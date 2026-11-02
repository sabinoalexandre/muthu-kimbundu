"""Translation service: coordinates translation workflows and storage."""

from typing import Optional

from src.core.translator import Translator
from src.core.translation_result import TranslationResult
from src.services.storage_service import StorageService


class TranslationService:
    """Runs translation requests and records successful history entries."""

    def __init__(
        self,
        translator: Translator,
        storage_service: Optional[StorageService] = None,
    ) -> None:
        self.translator = translator
        self.storage_service = storage_service

    @property
    def translator_name(self) -> str:
        """Return the name of the underlying translator."""
        return self.translator.provider_name

    def translate(
        self, text: str, source: str, target: str
    ) -> TranslationResult:
        """Translate ``text`` and handle failures gracefully."""
        try:
            result = self.translator.translate(text, source, target)
        except Exception as exc:  # noqa: BLE001 - never crash the interface layer
            result = TranslationResult.error(
                (text or "").strip(),
                source or "",
                target or "",
                f"Unexpected translation failure: {exc}",
                method=self.translator.provider_name,
            )

        if (
            self.storage_service is not None
            and result.is_success
            and result.translated_text
        ):
            try:
                self.storage_service.save_history(
                    original_text=result.original_text,
                    translated_text=result.translated_text,
                    source_language=result.source_language,
                    target_language=result.target_language,
                    provider=result.method,
                    verification_status=result.verification_status,
                )
            except Exception as exc:  # noqa: BLE001 - persistence must not hide a translation
                result.notes.append(f"Tradução concluída, mas o histórico não foi guardado: {exc}")
        return result
