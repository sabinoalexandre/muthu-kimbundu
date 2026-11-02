"""Unit tests for language switching behaviour."""

import pytest

from src.core.language import (
    KIMBUNDU,
    PORTUGUESE,
    SUPPORTED_LANGUAGES,
    get_language_name,
    get_language_pair,
    get_opposite,
    is_supported,
)


def test_opposite_language_of_portuguese_is_kimbundu():
    assert get_opposite(PORTUGUESE) == KIMBUNDU


def test_opposite_language_of_kimbundu_is_portuguese():
    assert get_opposite(KIMBUNDU) == PORTUGUESE


def test_supported_languages_are_the_portuguese_kimbundu_pair():
    assert SUPPORTED_LANGUAGES == (PORTUGUESE, KIMBUNDU)
    assert is_supported(PORTUGUESE) is True
    assert is_supported(KIMBUNDU) is True
    assert is_supported("fr") is False


def test_language_names_are_human_readable():
    assert get_language_name(PORTUGUESE) == "Portuguese"
    assert get_language_name(KIMBUNDU) == "Kimbundu"


def test_valid_language_pair_is_accepted():
    assert get_language_pair(PORTUGUESE, KIMBUNDU) == (PORTUGUESE, KIMBUNDU)


def test_invalid_language_pairs_are_rejected():
    with pytest.raises(ValueError):
        get_language_pair(PORTUGUESE, PORTUGUESE)
    with pytest.raises(ValueError):
        get_language_pair("fr", "kimbundu")
