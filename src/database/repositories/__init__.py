"""Database repositories."""

from src.database.repositories.history_repository import HistoryRepository
from src.database.repositories.favorites_repository import FavoritesRepository
from src.database.repositories.dictionary_repository import DictionaryRepository

__all__ = [
    "HistoryRepository",
    "FavoritesRepository",
    "DictionaryRepository",
]
