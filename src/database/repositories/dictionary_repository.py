"""Dictionary repository."""

import json
import sqlite3
from typing import List, Optional

from src.database.models import DictionaryEntry


class DictionaryRepository:
    """Data access for the local dictionary table."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def add(self, entry: DictionaryEntry) -> DictionaryEntry:
        """Insert a new dictionary entry and return it with its id."""
        cursor = self.connection.execute(
            """
            INSERT INTO dictionary (
                kimbundu_term, portuguese_translation, definition, alternative_meanings,
                examples, grammatical_category, regional_variation, verification_status,
                source_reference, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                entry.kimbundu_term,
                entry.portuguese_translation,
                entry.definition,
                json.dumps(entry.alternative_meanings or []),
                json.dumps(entry.examples or []),
                entry.grammatical_category,
                entry.regional_variation,
                entry.verification_status,
                entry.source_reference,
                entry.timestamp.isoformat() if entry.timestamp else "",
            ),
        )
        self.connection.commit()
        entry.id = cursor.lastrowid
        return entry

    def find_all(self, limit: int = 500) -> List[DictionaryEntry]:
        """Return dictionary entries."""
        cursor = self.connection.execute(
            "SELECT * FROM dictionary ORDER BY id LIMIT ?", (limit,)
        )
        return [DictionaryEntry.from_row(row) for row in cursor.fetchall()]

    def find_by_id(self, entry_id: int) -> Optional[DictionaryEntry]:
        """Return a single dictionary entry by id."""
        cursor = self.connection.execute(
            "SELECT * FROM dictionary WHERE id = ?", (entry_id,)
        )
        row = cursor.fetchone()
        return DictionaryEntry.from_row(row) if row is not None else None
