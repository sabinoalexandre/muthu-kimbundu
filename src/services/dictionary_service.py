"""Multilingual dictionary service."""

from typing import List, Optional

from src.core.language import KIKONGO, KIMBUNDU, PORTUGUESE, UMBUNDU
from src.database.models import DictionaryEntry
from src.providers.dictionary_provider import LocalDictionaryProvider


class DictionaryService:
    """Searches the local multilingual dictionary."""

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

        Searches the Kikongo, Kimbundu, Umbundu and Portuguese terms in each entry.
        """
        term = (query or "").strip().lower()
        if not term:
            return []

        matches: List[DictionaryEntry] = []
        for entry in self.dictionary_provider.entries:
            kimbundu_term = str(entry.get("kimbundu_term") or "").lower()
            kikongo_term = str(entry.get("kikongo_term") or "").lower()
            umbundu_term = str(entry.get("umbundu_term") or "").lower()
            portuguese_translation = (
                str(entry.get("portuguese_translation") or "").lower()
            )
            kimbundu_match = term in kimbundu_term
            kikongo_match = term in kikongo_term
            umbundu_match = term in umbundu_term
            portuguese_match = term in portuguese_translation
            if source_language == KIMBUNDU and not kimbundu_match:
                continue
            if source_language == KIKONGO and not kikongo_match:
                continue
            if source_language == UMBUNDU and not umbundu_match:
                continue
            if source_language == PORTUGUESE and not portuguese_match:
                continue
            if source_language is None and not (
                kimbundu_match or kikongo_match or umbundu_match or portuguese_match
            ):
                continue
            matches.append(DictionaryEntry.from_mapping(entry))
            if len(matches) >= limit:
                break

        return matches
