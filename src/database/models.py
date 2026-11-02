"""Database models for history, favorites and dictionary entries."""

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, List, Optional


@dataclass
class HistoryEntry:
    """A single saved translation request/result."""

    id: Optional[int] = None
    original_text: str = ""
    translated_text: str = ""
    source_language: str = ""
    target_language: str = ""
    provider: Optional[str] = None
    verification_status: str = "unknown"
    timestamp: Optional[datetime] = None

    def __post_init__(self) -> None:
        if self.timestamp is None:
            self.timestamp = datetime.now()

    @classmethod
    def from_row(cls, row: Any) -> "HistoryEntry":
        """Create an instance from a database row."""
        return cls(
            id=row["id"],
            original_text=row["original_text"],
            translated_text=row["translated_text"],
            source_language=row["source_language"],
            target_language=row["target_language"],
            provider=row["provider"],
            verification_status=row["verification_status"],
            timestamp=_as_datetime(row["timestamp"]),
        )

    def to_row(self) -> tuple:
        """Return the database column values."""
        return (
            self.id,
            self.original_text,
            self.translated_text,
            self.source_language,
            self.target_language,
            self.provider,
            self.verification_status,
            self.timestamp.isoformat() if self.timestamp else "",
        )


@dataclass
class Favorite:
    """A user saved translation or expression."""

    id: Optional[int] = None
    original_text: str = ""
    translated_text: str = ""
    source_language: str = ""
    target_language: str = ""
    timestamp: Optional[datetime] = None

    def __post_init__(self) -> None:
        if self.timestamp is None:
            self.timestamp = datetime.now()

    @classmethod
    def from_row(cls, row: Any) -> "Favorite":
        """Create an instance from a database row."""
        return cls(
            id=row["id"],
            original_text=row["original_text"],
            translated_text=row["translated_text"],
            source_language=row["source_language"],
            target_language=row["target_language"],
            timestamp=_as_datetime(row["timestamp"]),
        )


@dataclass
class DictionaryEntry:
    """A bilingual dictionary entry."""

    id: Optional[int] = None
    kimbundu_term: str = ""
    portuguese_translation: str = ""
    definition: Optional[str] = None
    alternative_meanings: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)
    grammatical_category: Optional[str] = None
    regional_variation: Optional[str] = None
    verification_status: str = "unverified"
    source_reference: Optional[str] = None
    timestamp: Optional[datetime] = None

    def __post_init__(self) -> None:
        if self.timestamp is None:
            self.timestamp = datetime.now()

    @classmethod
    def from_mapping(cls, mapping: dict) -> "DictionaryEntry":
        """Create an instance from a dictionary resource mapping."""
        return cls(
            kimbundu_term=str(mapping.get("kimbundu_term") or ""),
            portuguese_translation=str(mapping.get("portuguese_translation") or ""),
            definition=mapping.get("definition"),
            alternative_meanings=list(mapping.get("alternative_meanings") or []),
            examples=list(mapping.get("examples") or []),
            grammatical_category=mapping.get("grammatical_category"),
            regional_variation=mapping.get("regional_variation"),
            verification_status=mapping.get("verification_status") or "unverified",
            source_reference=mapping.get("source_reference"),
        )

    @classmethod
    def from_row(cls, row: Any) -> "DictionaryEntry":
        """Create an instance from a database row."""
        return cls(
            id=row["id"],
            kimbundu_term=row["kimbundu_term"],
            portuguese_translation=row["portuguese_translation"],
            definition=row["definition"],
            alternative_meanings=_as_list(row["alternative_meanings"]),
            examples=_as_list(row["examples"]),
            grammatical_category=row["grammatical_category"],
            regional_variation=row["regional_variation"],
            verification_status=row["verification_status"],
            source_reference=row["source_reference"],
            timestamp=_as_datetime(row["timestamp"]),
        )

    def to_row(self) -> tuple:
        """Return the database column values."""
        return (
            self.id,
            self.kimbundu_term,
            self.portuguese_translation,
            self.definition,
            json.dumps(self.alternative_meanings or []),
            json.dumps(self.examples or []),
            self.grammatical_category,
            self.regional_variation,
            self.verification_status,
            self.source_reference,
            self.timestamp.isoformat() if self.timestamp else "",
        )


def _as_datetime(value: Optional[str]) -> Optional[datetime]:
    """Parse an ISO timestamp coming from SQLite."""
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value))
    except ValueError:
        return None


def _as_list(value: Optional[str]) -> List[str]:
    """Parse a JSON encoded list coming from SQLite."""
    if not value:
        return []
    if isinstance(value, list):
        return list(value)
    try:
        parsed = json.loads(value)
    except (TypeError, ValueError):
        return []
    if isinstance(parsed, list):
        return [str(item) for item in parsed]
    return [str(parsed)]
