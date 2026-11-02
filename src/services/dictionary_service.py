"""Bilingual dictionary service."""

from typing import List, Optional

from src.core.language import KIMBUNDU, PORTUGUESE
from src.database.models import DictionaryEntry
from src.providers.dictionary_provider import LocalDictionaryProvider


class DictionaryService:
    """Searches the local bilingual dictionary in both directions."""

    def __init__(self, dictionary_provider: LocalDictionaryProvider) -> None:
        self.dictionary_provider = dictionary_provider

    def search(
        self,
        query: str,
        source_language: Optional[str] = None,
        target_language: Optional[str] = None,
        limit: int = 50,
    ) -> List[DictionaryEntry]:
        """Return dictionary entries matching ``query``.

        Searches Kimbundu -> Portuguese and Portuguese -> Kimbundu entries.
        """
        term = (query or "").strip().lower()
        if not term:
            return []

        matches: List[DictionaryEntry] = []
        for entry in self.dictionary_provider.entries:
            kimbundu_term = str(entry.get("kimbundu_term") or "").lower()
            portuguese_translation = (
                str(entry.get("portuguese_translation") or "").lower()
            )
            kimbundu_match = term in kimbundu_term
            portuguese_match = term in portuguese_translation
            if source_language == KIMBUNDU and not kimbundu_match:
                continue
            if source_language == PORTUGUESE and not portuguese_match:
                continue
            if source_language is None and not (kimbundu_match or portuguese_match):
                continue
            matches.append(DictionaryEntry.from_mapping(entry))
            if len(matches) >= limit:
                break

        return matches
