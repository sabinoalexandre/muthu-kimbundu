"""Unit tests for the input validators."""

from src.core.language import get_language_name, get_opposite, is_supported
from src.core.validators import (
    MAX_TEXT_LENGTH,
    validate_language_pair,
    validate_text,
    validate_translation_request,
)


def test_validate_text_accepts_non_empty_text():
    assert validate_text("  olá mundo  ") is None


def test_validate_text_rejects_empty_text():
    assert validate_text("") is not None
    assert validate_text("   ") is not None
    assert validate_text(None) is not None


def test_validate_text_rejects_oversized_text():
    assert validate_text("a" * (MAX_TEXT_LENGTH + 1)) is not None
    assert validate_text("a" * MAX_TEXT_LENGTH) is None


def test_validate_language_pair_accepts_supported_pair():
    assert validate_language_pair("pt", "kimbundu") is None


def test_validate_language_pair_rejects_unsupported_languages():
    assert validate_language_pair("fr", "kimbundu") is not None
    assert validate_language_pair("pt", "xx") is not None


def test_validate_language_pair_rejects_same_language():
    assert validate_language_pair("pt", "pt") is not None


def test_validate_translation_request_combines_checks():
    assert validate_translation_request("", "pt", "kimbundu") is not None
    assert validate_translation_request("texto", "pt", "pt") is not None
    assert validate_translation_request("texto", "pt", "kimbundu") is None


def test_language_helpers():
    assert is_supported("pt") is True
    assert is_supported("kimbundu") is True
    assert is_supported("fr") is False
    assert get_language_name("pt") == "Portuguese"
    assert get_language_name("kimbundu") == "Kimbundu"
    assert get_opposite("pt") == "kimbundu"
    assert get_opposite("kimbundu") == "pt"
