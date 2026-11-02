"""Translation result value object and reliability classification."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class TranslationStatus(str, Enum):
    """High level outcome of a translation attempt."""

    SUCCESS_VERIFIED = "success_verified"
    SUCCESS_DICTIONARY = "success_dictionary"
    SUCCESS_MACHINE = "success_machine"
    UNSUPPORTED = "unsupported"
    ERROR = "error"


VERIFICATION_STATUS_VERIFIED = "verified"
VERIFICATION_STATUS_UNVERIFIED = "unverified"
VERIFICATION_STATUS_UNKNOWN = "unknown"

STATUS_LABELS = {
    TranslationStatus.SUCCESS_VERIFIED: "Tradução verificada",
    TranslationStatus.SUCCESS_DICTIONARY: "Resultado do dicionário",
    TranslationStatus.SUCCESS_MACHINE: "Tradução automática",
    TranslationStatus.UNSUPPORTED: "Sem correspondência · texto original mantido",
    TranslationStatus.ERROR: "Não foi possível concluir a consulta",
}


def get_status_label(status) -> str:
    """Return a human readable label for a translation status."""
    return STATUS_LABELS.get(status, str(status))


@dataclass
class TranslationResult:
    """Outcome of a translation or dictionary lookup."""

    original_text: str = ""
    translated_text: str = ""
    source_language: str = ""
    target_language: str = ""
    status: TranslationStatus = TranslationStatus.ERROR
    method: Optional[str] = None
    verification_status: str = VERIFICATION_STATUS_UNKNOWN
    confidence: float = 0.0
    alternatives: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    timestamp: Optional[datetime] = None

    @property
    def is_success(self) -> bool:
        """Return ``True`` when a usable translation was produced."""
        return self.status in (
            TranslationStatus.SUCCESS_VERIFIED,
            TranslationStatus.SUCCESS_DICTIONARY,
            TranslationStatus.SUCCESS_MACHINE,
        )

    @property
    def is_unsupported(self) -> bool:
        """Return ``True`` when the expression has no reliable translation."""
        return self.status is TranslationStatus.UNSUPPORTED

    @property
    def is_error(self) -> bool:
        """Return ``True`` when the translation failed."""
        return self.status is TranslationStatus.ERROR

    @property
    def is_verified(self) -> bool:
        """Return ``True`` when the translation carries verified status."""
        return self.verification_status == VERIFICATION_STATUS_VERIFIED

    @classmethod
    def verified(
        cls,
        original_text: str,
        translated_text: str,
        source_language: str,
        target_language: str,
        method: Optional[str] = None,
        confidence: float = 1.0,
        alternatives: Optional[List[str]] = None,
        notes: Optional[List[str]] = None,
    ) -> "TranslationResult":
        """Build a successful, verified translation result."""
        return cls(
            original_text=original_text or "",
            translated_text=translated_text or "",
            source_language=source_language or "",
            target_language=target_language or "",
            status=TranslationStatus.SUCCESS_VERIFIED,
            method=method,
            verification_status=VERIFICATION_STATUS_VERIFIED,
            confidence=confidence,
            alternatives=list(alternatives or []),
            notes=list(notes or []),
        )

    @classmethod
    def from_dictionary(
        cls,
        original_text: str,
        translated_text: str,
        source_language: str,
        target_language: str,
        entry: Any,
    ) -> "TranslationResult":
        """Build a result from a bilingual dictionary entry."""
        if isinstance(entry, dict):
            verification_status = entry.get("verification_status") or VERIFICATION_STATUS_UNVERIFIED
            source_reference = entry.get("source_reference")
            alternatives = entry.get("alternative_meanings") or []
            examples = entry.get("examples") or []
        else:
            verification_status = getattr(entry, "verification_status", None) or VERIFICATION_STATUS_UNVERIFIED
            source_reference = getattr(entry, "source_reference", None)
            alternatives = getattr(entry, "alternative_meanings", None) or []
            examples = getattr(entry, "examples", None) or []

        confidence = 1.0 if verification_status == VERIFICATION_STATUS_VERIFIED else 0.5
        notes = []
        if source_reference:
            notes.append(f"Source: {source_reference}")
        if verification_status != VERIFICATION_STATUS_VERIFIED:
            notes.append("Dictionary entry has not been verified by a Kimbundu speaker yet.")

        return cls(
            original_text=original_text or "",
            translated_text=translated_text or "",
            source_language=source_language or "",
            target_language=target_language or "",
            status=TranslationStatus.SUCCESS_DICTIONARY,
            method="LocalDictionaryProvider",
            verification_status=verification_status,
            confidence=confidence,
            alternatives=list(alternatives or []),
            notes=notes,
        )

    @classmethod
    def unsupported(
        cls,
        original_text: str,
        source_language: str,
        target_language: str,
        reason: str,
    ) -> "TranslationResult":
        """Build an explicit unsupported translation result."""
        return cls(
            original_text=original_text or "",
            translated_text=original_text or "",
            source_language=source_language or "",
            target_language=target_language or "",
            status=TranslationStatus.UNSUPPORTED,
            verification_status=VERIFICATION_STATUS_UNKNOWN,
            confidence=0.0,
            notes=[reason] if reason else [],
        )

    @classmethod
    def error(
        cls,
        original_text: str,
        source_language: str,
        target_language: str,
        reason: str,
        method: Optional[str] = None,
    ) -> "TranslationResult":
        """Build a failed translation result."""
        return cls(
            original_text=original_text or "",
            translated_text="",
            source_language=source_language or "",
            target_language=target_language or "",
            status=TranslationStatus.ERROR,
            method=method,
            verification_status=VERIFICATION_STATUS_UNKNOWN,
            confidence=0.0,
            notes=[reason],
        )
