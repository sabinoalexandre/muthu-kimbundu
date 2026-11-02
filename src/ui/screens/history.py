"""Translation history screen."""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField

from src.database.models import HistoryEntry
from src.services.storage_service import StorageService
from src.ui.widgets.buttons import create_mdbutton


class HistoryScreen(MDScreen):
    """Screen listing the saved translation history."""

    storage_service = None

    entries = ListProperty([])
    filtered_entries = ListProperty([])

    def __init__(self, storage_service=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.storage_service = storage_service
        self.entries = []
        self.filtered_entries = []
        self._build_ui()

    def _build_ui(self) -> None:
        root = BoxLayout(orientation="vertical")
        header = MDLabel(
            text="History",
            size_hint_y=None,
            height=dp(40),
            halign="center",
            valign="middle",
        )
        self.search_field = MDTextField(
            hint_text="Search history",
            size_hint_y=None,
            height=dp(48),
        )
        self.search_button = create_mdbutton(
            "Search",
            on_release=self.on_search,
            size_hint_x=None,
            width=dp(120),
        )
        search_row = BoxLayout(orientation="horizontal", spacing=dp(8))
        search_row.add_widget(self.search_field)
        search_row.add_widget(self.search_button)
        self.entries_container = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
        )
        self.clear_button = create_mdbutton(
            "Clear history",
            on_release=self.on_clear_history,
            size_hint_x=None,
            width=dp(160),
        )
        root.add_widget(header)
        root.add_widget(search_row)
        root.add_widget(self.entries_container)
        root.add_widget(self.clear_button)
        self.add_widget(root)
        self.refresh()

    def refresh(self) -> None:
        """Reload history entries from the storage service."""
        self.entries = self.storage_service.get_history(limit=100)
        self._apply_filter()

    def _apply_filter(self) -> None:
        """Filter the visible history entries by the search term."""
        term = (self.search_field.text or "").strip().lower()
        if not term:
            self.filtered_entries = list(self.entries)
            return
        self.filtered_entries = [
            entry
            for entry in self.entries
            if term in entry.original_text.lower()
            or term in entry.translated_text.lower()
            or term in (entry.provider or "").lower()
        ]

    def on_search(self, *args) -> None:
        """Run the history search."""
        self._apply_filter()
        self._rebuild_rows()

    def _rebuild_rows(self) -> None:
        """Rebuild the history rows from the filtered entries."""
        self.entries_container.clear_widgets()
        for entry in self.filtered_entries:
            self.entries_container.add_widget(self._build_entry_row(entry))

    def _build_entry_row(self, entry: HistoryEntry):
        row = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(170),
            padding=[4, 4],
            spacing=dp(2),
        )
        row.add_widget(MDLabel(text=entry.original_text, size_hint_y=None, height=dp(20), halign="left", valign="middle"))
        row.add_widget(MDLabel(text=entry.translated_text, size_hint_y=None, height=dp(20), halign="left", valign="middle"))
        row.add_widget(MDLabel(text=f"{entry.source_language} -> {entry.target_language}", size_hint_y=None, height=dp(20), halign="left", valign="middle"))
        row.add_widget(MDLabel(text=f"Status: {entry.verification_status}", size_hint_y=None, height=dp(20), halign="left", valign="middle"))
        row.add_widget(MDLabel(text=f"Provider: {entry.provider}", size_hint_y=None, height=dp(20), halign="left", valign="middle"))
        row.add_widget(MDLabel(text=f"Date: {entry.timestamp}", size_hint_y=None, height=dp(20), halign="left", valign="middle"))
        delete_button = create_mdbutton(
            "Delete",
            on_release=lambda entry_id=entry.id: self.on_delete(entry_id),
            size_hint_x=None,
            width=dp(100),
        )
        row.add_widget(delete_button)
        return row

    def on_delete(self, entry_id) -> None:
        """Delete a single history entry."""
        if self.storage_service is None or entry_id is None:
            return
        self.storage_service.delete_history(entry_id)
        self.refresh()

    def on_clear_history(self, *args) -> None:
        """Clear the complete translation history."""
        if self.storage_service is None:
            return
        self.storage_service.clear_history()
        self.refresh()
