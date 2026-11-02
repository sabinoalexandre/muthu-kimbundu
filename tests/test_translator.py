"""Unit tests for the MUTHU translation engine and providers."""

import json
from pathlib import Path

from src.core.exceptions import ProviderError, UnsupportedTranslationError
from src.core.translation_result import TranslationResult, TranslationStatus, get_status_label
from src.core.translator import Translator
from src.providers.dictionary_provider import LocalDictionaryProvider
from src.providers.machine_translation_provider import MachineTranslationProvider


def write_dictionary(tmp_path, entries):
    path = tmp_path / "dictionary.json"
    path.write_text(json.dumps({"version": 1, "entries": entries}), encoding="utf-8")
    return str(path)


def make_provider(tmp_path, entries):
    return LocalDictionaryProvider(dictionary_path=write_dictionary(tmp_path, entries))


def make_translator(provider):
    return Translator(provider=provider)


def verified_entry():
    return {
        "id": 1,
        "kimbundu_term": "mukanda",
        "portuguese_translation": "familia",
        "definition": "Family.",
        "alternative_meanings": [],
        "examples": [],
        "grammatical_category": "noun",
        "regional_variation": None,
        "verification_status": "verified",
        "source_reference": "Linguistic review",
        "timestamp": "2026-11-02T00:00:00",
    }


def test_translates_portuguese_to_kimbundu_with_dictionary_entry(tmp_path):
    provider = make_provider(tmp_path, [verified_entry()])
    result = make_translator(provider).translate("familia", "pt", "kimbundu")
    assert result.is_success
    assert result.status is TranslationStatus.SUCCESS_DICTIONARY
    assert result.translated_text == "mukanda"
    assert result.source_language == "pt"
    assert result.target_language == "kimbundu"
    assert result.method == "LocalDictionaryProvider"
    assert result.is_verified


def test_translates_kimbundu_to_portuguese_with_dictionary_entry(tmp_path):
    provider = make_provider(tmp_path, [verified_entry()])
    result = make_translator(provider).translate("mukanda", "kimbundu", "pt")
    assert result.is_success
    assert result.status is TranslationStatus.SUCCESS_DICTIONARY
    assert result.translated_text == "familia"
    assert result.source_language == "kimbundu"
    assert result.target_language == "pt"


def test_unverified_entry_is_not_marked_as_verified(tmp_path):
    provider = make_provider(
        tmp_path,
        [
            {
                "id": 1,
                "kimbundu_term": "mukanda",
                "portuguese_translation": "familia",
                "verification_status": "unverified",
                "source_reference": "Pending review",
                "alternative_meanings": [],
                "examples": [],
            }
        ],
    )
    result = make_translator(provider).translate("mukanda", "kimbundu", "pt")
    assert result.is_success
    assert not result.is_verified
    assert result.verification_status == "unverified"
    assert result.confidence < 1.0
    assert any("verif" in note.lower() for note in result.notes)


def test_unsupported_expression_returns_unsupported_result(tmp_path):
    provider = make_provider(tmp_path, [])
    translator = make_translator(provider)
    result = translator.translate("xyzabc", "pt", "kimbundu")
    assert result.is_unsupported
    assert not result.is_success
    assert result.status is TranslationStatus.UNSUPPORTED


def test_provider_error_is_converted_into_error_result():
    provider = MachineTranslationProvider()
    translator = make_translator(provider)
    result = translator.translate("familia", "pt", "kimbundu")
    assert result.is_error
    assert not result.is_success
    assert result.status is TranslationStatus.ERROR


def test_invalid_language_pair_returns_error_result(tmp_path):
    provider = make_provider(tmp_path, [verified_entry()])
    translator = make_translator(provider)
    result = translator.translate("familia", "pt", "pt")
    assert result.is_error
    assert "different" in result.notes[0].lower()
