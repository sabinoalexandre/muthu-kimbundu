"""Favorites screen."""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField

from src.database.models import Favorite
from src.services.storage_service import StorageService
from src.ui.widgets.buttons import create_mdbutton


class FavoritesScreen(MDScreen):
    """Screen listing the user saved favorites."""

    storage_service = None

    favorites = ListProperty([])
    filtered_favorites = ListProperty([])
    entries = ListProperty([])

    def __init__(self, storage_service=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.storage_service = storage_service
        self.favorites = []
        self.entries = []
        self.filtered_favorites = []
        self._build_ui()

    def _build_ui(self) -> None:
        root = BoxLayout(orientation="vertical")
        header = MDLabel(
            text="Favorites",
            size_hint_y=None,
            height=dp(40),
            halign="center",
            valign="middle",
        )
        self.search_field = MDTextField(
            hint_text="Search favorites",
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
            "Clear favorites",
            on_release=self.on_clear,
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
        """Reload the favorites from the storage service."""
        self.favorites = self.storage_service.get_favorites()
        self.entries = self.favorites
        self._apply_filter()

    def _apply_filter(self) -> None:
        """Filter the visible favorites by the search term."""
        term = (self.search_field.text or "").strip().lower()
        if not term:
            self.filtered_favorites = list(self.favorites)
            return
        self.filtered_favorites = [
            favorite
            for favorite in self.favorites
            if term in favorite.original_text.lower()
            or term in favorite.translated_text.lower()
        ]

    def on_search(self, *args) -> None:
        """Run the favorites search."""
        self._apply_filter()
        self._rebuild_rows()

    def _rebuild_rows(self) -> None:
        """Rebuild the favorites rows from the filtered entries."""
        self.entries_container.clear_widgets()
        for favorite in self.filtered_favorites:
            self.entries_container.add_widget(self._build_entry_row(favorite))

    def _build_entry_row(self, favorite) -> BoxLayout:
        row = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(110), padding=[4, 4], spacing=dp(2))
        row.add_widget(MDLabel(text=favorite.original_text, size_hint_y=None, height=dp(20), halign="left", valign="middle"))
        row.add_widget(MDLabel(text=favorite.translated_text, size_hint_y=None, height=dp(20), halign="left", valign="middle"))
        copy_button = create_mdbutton(
            "Copy",
            on_release=lambda fav=favorite: self.on_copy(fav),
            size_hint_x=None,
            width=dp(100),
        )
        remove_button = create_mdbutton(
            "Remove",
            on_release=lambda fav=favorite: self.on_remove(fav),
            size_hint_x=None,
            width=dp(100),
        )
        actions = BoxLayout(orientation="horizontal", spacing=dp(8))
        actions.add_widget(copy_button)
        actions.add_widget(remove_button)
        row.add_widget(actions)
        return row

    def on_copy(self, favorite) -> None:
        """Copy a favorite translation to the clipboard."""
        from kivy.clipboard import Clipboard

        Clipboard.copy(favorite.translated_text)

    def on_remove(self, favorite) -> None:
        """Remove a single favorite."""
        if favorite is None or favorite.id is None:
            return
        self.storage_service.remove_favorite(favorite.id)
        self.refresh()

    def on_clear(self, *args) -> None:
        """Clear all favorites."""
        self.storage_service.clear_favorites()
        self.refresh()
