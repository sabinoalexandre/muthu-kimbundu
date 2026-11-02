"""SQLite database access helpers."""

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATABASE_PATH = BASE_DIR / "data" / "muthu.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS translation_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_text TEXT NOT NULL,
    translated_text TEXT NOT NULL,
    source_language TEXT NOT NULL,
    target_language TEXT NOT NULL,
    provider TEXT,
    verification_status TEXT NOT NULL,
    timestamp TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_text TEXT NOT NULL,
    translated_text TEXT NOT NULL,
    source_language TEXT NOT NULL,
    target_language TEXT NOT NULL,
    timestamp TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS dictionary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kimbundu_term TEXT NOT NULL,
    portuguese_translation TEXT NOT NULL,
    definition TEXT,
    alternative_meanings TEXT,
    examples TEXT,
    grammatical_category TEXT,
    regional_variation TEXT,
    verification_status TEXT NOT NULL,
    source_reference TEXT,
    timestamp TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""


def get_connection() -> sqlite3.Connection:
    """Return a new SQLite connection with the row factory configured."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database() -> None:
    """Create the application database schema when it does not exist yet."""
    connection = get_connection()
    try:
        connection.executescript(SCHEMA)
        connection.commit()
    finally:
        connection.close()
