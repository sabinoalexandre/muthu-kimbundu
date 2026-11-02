"""Unit tests for the SQLite storage workflows."""

from src.database import db
from src.database.models import Favorite, HistoryEntry
from src.services.storage_service import StorageService


def make_storage(tmp_path):
    db.DATABASE_PATH = db.Path(str(tmp_path / "muthu_test.db"))
    db.initialize_database()
    storage = StorageService(database_path=str(tmp_path / "muthu_test.db"))
    return storage


def test_save_and_retrieve_history(tmp_path):
    storage = make_storage(tmp_path)
    saved = storage.save_history(
        original_text="familia",
        translated_text="mukanda",
        source_language="pt",
        target_language="kimbundu",
        provider="LocalDictionaryProvider",
        verification_status="verified",
    )
    history = storage.get_history()
    assert len(history) == 1
    assert history[0].original_text == "familia"
    assert history[0].translated_text == "mukanda"
    assert history[0].source_language == "pt"
    assert history[0].target_language == "kimbundu"
    assert history[0].provider == "LocalDictionaryProvider"
    assert history[0].verification_status == "verified"
    storage.close()


def test_delete_and_clear_history(tmp_path):
    storage = make_storage(tmp_path)
    saved = storage.save_history(
        original_text="familia",
        translated_text="mukanda",
        source_language="pt",
        target_language="kimbundu",
        verification_status="verified",
    )
    assert storage.delete_history(saved.id) is True
    assert storage.get_history() == []
    saved = storage.save_history(
        original_text="texto",
        translated_text="texto traduzido",
        source_language="pt",
        target_language="kimbundu",
        verification_status="verified",
    )
    assert storage.clear_history() is True
    assert storage.get_history() == []
    storage.close()


def test_add_and_remove_favorites(tmp_path):
    storage = make_storage(tmp_path)
    favorite = storage.add_favorite(
        original_text="familia",
        translated_text="mukanda",
        source_language="pt",
        target_language="kimbundu",
    )
    favorites = storage.get_favorites()
    assert len(favorites) == 1
    assert favorites[0].translated_text == "mukanda"
    assert storage.remove_favorite(favorite.id) is True
    second = storage.add_favorite(
        original_text="palavra",
        translated_text="palavra traduzida",
        source_language="pt",
        target_language="kimbundu",
    )
    assert storage.clear_favorites() is True
    assert storage.get_favorites() == []
    assert storage.remove_favorite(second.id) is False
    storage.close()


def test_save_and_get_preferences(tmp_path):
    storage = make_storage(tmp_path)
    storage.save_preference("theme", "dark")
    assert storage.get_preference("theme", "light") == "dark"
    assert storage.get_preferences()["theme"] == "dark"
    storage.close()
