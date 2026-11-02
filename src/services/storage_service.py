"""Storage service: persistence workflows for history, favorites and settings."""

import sqlite3
from typing import Any, Dict, List, Optional

from src.database import db
from src.database.models import Favorite, HistoryEntry
from src.database.repositories.dictionary_repository import DictionaryRepository
from src.database.repositories.favorites_repository import FavoritesRepository
from src.database.repositories.history_repository import HistoryRepository


class StorageService:
    """Coordinates database repositories and user preferences."""

    def __init__(self, database_path: Optional[str] = None) -> None:
        if database_path:
            from src.database import db as db_module

            db_module.DATABASE_PATH = db_module.Path(database_path)
        self.database_path = db.DATABASE_PATH
        db.initialize_database()
        self.connection = db.get_connection()
        self.history_repository = HistoryRepository(self.connection)
        self.favorites_repository = FavoritesRepository(self.connection)
        self.dictionary_repository = DictionaryRepository(self.connection)

    # ------------------------------------------------------------------
    # Translation history
    # ------------------------------------------------------------------
    def save_history(
        self,
        original_text: str,
        translated_text: str,
        source_language: str,
        target_language: str,
        provider: Optional[str] = None,
        verification_status: str = "unknown",
    ) -> HistoryEntry:
        """Persist a completed translation in the history."""
        entry = HistoryEntry(
            original_text=original_text,
            translated_text=translated_text,
            source_language=source_language,
            target_language=target_language,
            provider=provider,
            verification_status=verification_status,
        )
        # Translation requests run in worker threads. Give each write its own
        # connection because sqlite3 connections belong to their creating thread.
        connection = sqlite3.connect(str(self.database_path), timeout=10)
        connection.row_factory = sqlite3.Row
        try:
            return HistoryRepository(connection).save(entry)
        finally:
            connection.close()

    def get_history(self, limit: int = 100) -> List[HistoryEntry]:
        """Return the most recent translation history entries."""
        return self.history_repository.find_all(limit=limit)

    def delete_history(self, entry_id: int) -> bool:
        """Delete a single history entry."""
        return self.history_repository.delete(entry_id)

    def clear_history(self) -> bool:
        """Delete the complete translation history."""
        return self.history_repository.clear()

    # ------------------------------------------------------------------
    # Favorites
    # ------------------------------------------------------------------
    def add_favorite(
        self,
        original_text: str,
        translated_text: str,
        source_language: str,
        target_language: str,
    ) -> Favorite:
        """Save a translation or expression as favorite."""
        favorite = Favorite(
            original_text=original_text,
            translated_text=translated_text,
            source_language=source_language,
            target_language=target_language,
        )
        return self.favorites_repository.add(favorite)

    def get_favorites(self) -> List[Favorite]:
        """Return all saved favorites."""
        return self.favorites_repository.list_all()

    def remove_favorite(self, favorite_id: int) -> bool:
        """Remove a single favorite."""
        return self.favorites_repository.remove(favorite_id)

    def clear_favorites(self) -> bool:
        """Remove every favorite."""
        return self.favorites_repository.clear()

    # ------------------------------------------------------------------
    # Settings
    # ------------------------------------------------------------------
    def save_preference(self, key: str, value: str) -> None:
        """Persist a single application preference."""
        self.connection.execute(
            """
            INSERT INTO settings (key, value) VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
            """,
            (key, value),
        )
        self.connection.commit()

    def get_preference(self, key: str, default: str = "") -> str:
        """Return a single application preference."""
        cursor = self.connection.execute(
            "SELECT value FROM settings WHERE key = ?", (key,)
        )
        row = cursor.fetchone()
        return row["value"] if row is not None else default

    def get_preferences(self) -> Dict[str, str]:
        """Return all stored application preferences."""
        cursor = self.connection.execute("SELECT key, value FROM settings")
        return {row["key"]: row["value"] for row in cursor.fetchall()}

    def close(self) -> None:
        """Close the underlying database connection."""
        self.connection.close()
