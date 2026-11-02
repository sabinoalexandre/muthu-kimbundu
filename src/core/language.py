"""Supported languages and language-pair helpers."""

PORTUGUESE = "pt"
KIMBUNDU = "kimbundu"

LANGUAGE_LABELS = {
    PORTUGUESE: "Portuguese",
    KIMBUNDU: "Kimbundu",
}

SUPPORTED_LANGUAGES = (PORTUGUESE, KIMBUNDU)


def is_supported(language: str) -> bool:
    """Return ``True`` when the language can be used by MUTHU."""
    return language in SUPPORTED_LANGUAGES


def get_language_name(language: str) -> str:
    """Return the human readable name of a supported language."""
    return LANGUAGE_LABELS.get(language, language)


def get_opposite(language: str) -> str:
    """Return the opposite language of the given supported language."""
    if language == PORTUGUESE:
        return KIMBUNDU
    if language == KIMBUNDU:
        return PORTUGUESE
    raise ValueError(f"Unsupported language: {language}")


def get_language_pair(source: str, target: str) -> tuple[str, str]:
    """Validate a source/target pair and return it when acceptable.

    Raises:
        ValueError: when a language is unsupported or both languages match.
    """
    if source not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported source language: {source}")
    if target not in SUPPORTED_LANGUAGES:
        raise ValueError(f"Unsupported target language: {target}")
    if source == target:
        raise ValueError("Source and target languages must be different.")
    return source, target
