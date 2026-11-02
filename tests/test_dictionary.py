"""Unit tests for the bilingual dictionary service."""

from src.database.models import DictionaryEntry
from src.providers.dictionary_provider import LocalDictionaryProvider
from src.services.dictionary_service import DictionaryService


def make_service(entries):
    provider = LocalDictionaryProvider(
        dictionary_path="/tmp/opencode/muthu_test_dictionary.json"
    )
    provider.entries = entries
    return DictionaryService(dictionary_provider=provider)


def test_search_portuguese_to_kimbundu():
    service = make_service(
        [
            {
                "id": 1,
                "kimbundu_term": "mukanda",
                "portuguese_translation": "familia",
                "verification_status": "verified",
            },
            {
                "id": 2,
                "kimbundu_term": "kilunda",
                "portuguese_translation": "montanha",
                "verification_status": "unverified",
            },
        ]
    )
    results = service.search("familia", source_language="pt", target_language="kimbundu")
    assert len(results) == 1
    assert results[0].kimbundu_term == "mukanda"
    assert results[0].portuguese_translation == "familia"


def test_search_kimbundu_to_portuguese():
    service = make_service(
        [
            {
                "id": 1,
                "kimbundu_term": "mukanda",
                "portuguese_translation": "familia",
                "verification_status": "verified",
            },
        ]
    )
    results = service.search("mukanda", source_language="kimbundu", target_language="pt")
    assert len(results) == 1
    assert results[0].kimbundu_term == "mukanda"


def test_search_without_direction_returns_any_match():
    service = make_service(
        [
            {
                "id": 1,
                "kimbundu_term": "kilunda",
                "portuguese_translation": "montanha",
                "verification_status": "unverified",
            },
        ]
    )
    results = service.search("montanha")
    assert len(results) == 1
    assert results[0].portuguese_translation == "montanha"


def test_search_missing_entry_returns_no_results():
    service = make_service([])
    assert service.search("inexistente") == []


def test_dictionary_entry_conversion():
    entry = DictionaryEntry.from_mapping(
        {
            "kimbundu_term": "mukanda",
            "portuguese_translation": "familia",
            "verification_status": "verified",
            "source_reference": "Linguistic review",
        }
    )
    assert entry.verification_status == "verified"
    assert entry.source_reference == "Linguistic review"
    assert entry.alternative_meanings == []
    assert entry.examples == []
