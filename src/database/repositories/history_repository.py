"""Translation history repository."""

from typing import List, Optional

import sqlite3

from src.database.models import HistoryEntry


class HistoryRepository:
    """Data access for the translation history table."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def save(self, entry: HistoryEntry) -> HistoryEntry:
        """Insert a new history entry and return it with its id."""
        cursor = self.connection.execute(
            """
            INSERT INTO translation_history (
                original_text, translated_text, source_language, target_language,
                provider, verification_status, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                entry.original_text,
                entry.translated_text,
                entry.source_language,
                entry.target_language,
                entry.provider,
                entry.verification_status,
                entry.timestamp.isoformat() if entry.timestamp else "",
            ),
        )
        self.connection.commit()
        entry.id = cursor.lastrowid
        return entry

    def find_all(self, limit: int = 100) -> List[HistoryEntry]:
        """Return the most recent history entries."""
        cursor = self.connection.execute(
            "SELECT * FROM translation_history ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        return [HistoryEntry.from_row(row) for row in cursor.fetchall()]

    def find_by_id(self, entry_id: int) -> Optional[HistoryEntry]:
        """Return a single history entry by id."""
        cursor = self.connection.execute(
            "SELECT * FROM translation_history WHERE id = ?", (entry_id,)
        )
        row = cursor.fetchone()
        return HistoryEntry.from_row(row) if row is not None else None

    def delete(self, entry_id: int) -> bool:
        """Delete a single history entry."""
        cursor = self.connection.execute(
            "DELETE FROM translation_history WHERE id = ?", (entry_id,)
        )
        self.connection.commit()
        return cursor.rowcount > 0

    def clear(self) -> bool:
        """Delete every history entry."""
        cursor = self.connection.execute("DELETE FROM translation_history")
        self.connection.commit()
        return cursor.rowcount > 0
