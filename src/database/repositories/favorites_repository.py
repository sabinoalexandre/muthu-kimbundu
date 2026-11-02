"""User favorites repository."""

from typing import List, Optional

import sqlite3

from src.database.models import Favorite


class FavoritesRepository:
    """Data access for the favorites table."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.connection = connection

    def add(self, favorite: Favorite) -> Favorite:
        """Insert a new favorite and return it with its id."""
        cursor = self.connection.execute(
            """
            INSERT INTO favorites (
                original_text, translated_text, source_language, target_language, timestamp
            ) VALUES (?, ?, ?, ?, ?)
            """,
            (
                favorite.original_text,
                favorite.translated_text,
                favorite.source_language,
                favorite.target_language,
                favorite.timestamp.isoformat() if favorite.timestamp else "",
            ),
        )
        self.connection.commit()
        favorite.id = cursor.lastrowid
        return favorite

    def list_all(self) -> List[Favorite]:
        """Return all favorites."""
        cursor = self.connection.execute(
            "SELECT * FROM favorites ORDER BY id DESC"
        )
        return [Favorite.from_row(row) for row in cursor.fetchall()]

    def remove(self, favorite_id: int) -> bool:
        """Delete a single favorite."""
        cursor = self.connection.execute(
            "DELETE FROM favorites WHERE id = ?", (favorite_id,)
        )
        self.connection.commit()
        return cursor.rowcount > 0

    def clear(self) -> bool:
        """Delete every favorite."""
        cursor = self.connection.execute("DELETE FROM favorites")
        self.connection.commit()
        return cursor.rowcount > 0
