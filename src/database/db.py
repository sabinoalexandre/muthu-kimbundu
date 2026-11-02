"""SQLite database access helpers."""

import json
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
        _seed_dictionary(connection)
        connection.commit()
    finally:
        connection.close()


def _seed_dictionary(connection: sqlite3.Connection) -> None:
    """Copy sourced JSON entries into SQLite without duplicating existing rows."""
    dictionary_path = BASE_DIR / "data" / "dictionary.json"
    if not dictionary_path.exists():
        return
    try:
        with dictionary_path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return

    entries = payload.get("entries", []) if isinstance(payload, dict) else []
    if not isinstance(entries, list):
        return

    existing = {
        (str(row[0]).casefold().strip(), str(row[1]).casefold().strip())
        for row in connection.execute(
            "SELECT kimbundu_term, portuguese_translation FROM dictionary"
        )
    }
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        kimbundu_term = str(entry.get("kimbundu_term") or "").strip()
        portuguese_translation = str(entry.get("portuguese_translation") or "").strip()
        if not kimbundu_term or not portuguese_translation:
            continue
        key = (kimbundu_term.casefold(), portuguese_translation.casefold())
        if key in existing:
            continue
        connection.execute(
            """
            INSERT INTO dictionary (
                kimbundu_term, portuguese_translation, definition,
                alternative_meanings, examples, grammatical_category,
                regional_variation, verification_status, source_reference, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                kimbundu_term,
                portuguese_translation,
                entry.get("definition"),
                json.dumps(entry.get("alternative_meanings") or [], ensure_ascii=False),
                json.dumps(entry.get("examples") or [], ensure_ascii=False),
                entry.get("grammatical_category"),
                entry.get("regional_variation"),
                entry.get("verification_status") or "unverified",
                entry.get("source_reference"),
                entry.get("timestamp") or "",
            ),
        )
        existing.add(key)
