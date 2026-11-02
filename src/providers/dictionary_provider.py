"""Local bilingual dictionary translation provider."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.core.exceptions import UnsupportedTranslationError
from src.core.language import KIMBUNDU, PORTUGUESE
from src.core.translation_result import TranslationResult
from src.providers.base_provider import TranslationProvider

DEFAULT_DICTIONARY_PATH = (
    Path(__file__).resolve().parents[2] / "data" / "dictionary.json"
)


class LocalDictionaryProvider(TranslationProvider):
    """Dictionary based translation provider for Portuguese <-> Kimbundu."""

    def __init__(self, dictionary_path: Optional[str] = None) -> None:
        self.dictionary_path = (
            Path(dictionary_path) if dictionary_path else DEFAULT_DICTIONARY_PATH
        )
        self.entries: List[Dict[str, Any]] = self._load_entries()

    def _load_entries(self) -> List[Dict[str, Any]]:
        """Load the bilingual dictionary resource."""
        if not self.dictionary_path.exists():
            return []
        with open(self.dictionary_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        entries = data.get("entries") or []
        if not isinstance(entries, list):
            return []
        return [entry for entry in entries if isinstance(entry, dict)]

    @property
    def entry_count(self) -> int:
        """Return the number of loaded dictionary entries."""
        return len(self.entries)

    def get_entry(
        self,
        kimbundu_term: Optional[str] = None,
        portuguese_translation: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Return a single dictionary entry matching the given fields."""
        term = (kimbundu_term or "").strip().lower()
        translation = (portuguese_translation or "").strip().lower()
        for entry in self.entries:
            entry_term = str(entry.get("kimbundu_term") or "").strip().lower()
            entry_translation = str(entry.get("portuguese_translation") or "").strip().lower()
            if term and entry_term == term:
                return entry
            if translation and entry_translation == translation:
                return entry
        return None

    def translate(
        self, text: str, source: str, target: str
    ) -> TranslationResult:
        """Translate text using the local bilingual dictionary."""
        term = (text or "").strip()
        entry = None
        if source == KIMBUNDU and target == PORTUGUESE:
            entry = self.get_entry(kimbundu_term=term)
        elif source == PORTUGUESE and target == KIMBUNDU:
            entry = self.get_entry(portuguese_translation=term)

        if entry is None:
            raise UnsupportedTranslationError(
                f"No reliable Kimbundu dictionary entry is available for "
                f"'{term}'. The expression may be unsupported, newly coined, "
                "or not yet reviewed by a Kimbundu speaker."
            )

        if source == KIMBUNDU:
            translated_text = str(entry.get("portuguese_translation") or "")
        else:
            translated_text = str(entry.get("kimbundu_term") or "")
        return TranslationResult.from_dictionary(
            original_text=term,
            translated_text=translated_text,
            source_language=source,
            target_language=target,
            entry=entry,
        )

    def detect_language(self, text: str) -> Optional[str]:
        """Dictionary lookups cannot reliably detect language by themselves."""
        return None
