"""Database access layer."""

from src.database.db import get_connection, initialize_database

__all__ = ["get_connection", "initialize_database"]
