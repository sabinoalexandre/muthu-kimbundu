"""Input validation helpers."""

from typing import Optional

from src.core.language import SUPPORTED_LANGUAGES

MAX_TEXT_LENGTH = 5000


def validate_text(text: str) -> Optional[str]:
    """Validate source text, returning an error message or ``None``."""
    if text is None:
        return "Source text is required."
    stripped = str(text).strip()
    if not stripped:
        return "Source text cannot be empty."
    if len(stripped) > MAX_TEXT_LENGTH:
        return f"Source text cannot not exceed {MAX_TEXT_LENGTH} characters."
    return None


def validate_language_pair(source: str, target: str) -> Optional[str]:
    """Validate a source/target language pair, returning an error or ``None``."""
    if source not in SUPPORTED_LANGUAGES:
        return f"Unsupported source language: {source}"
    if target not in SUPPORTED_LANGUAGES:
        return f"Unsupported target language: {target}"
    if source == target:
        return "Source and target languages must be different."
    return None


def validate_translation_request(
    text: str, source: str, target: str
) -> Optional[str]:
    """Validate a complete translation request."""
    error = validate_language_pair(source, target)
    if error is not None:
        return error
    return validate_text(text)
