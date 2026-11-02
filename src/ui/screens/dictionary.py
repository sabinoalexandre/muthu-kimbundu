"""Bilingual dictionary screen."""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField

from src.database.models import DictionaryEntry
from src.services.dictionary_service import DictionaryService
from src.ui.widgets.buttons import create_mdbutton
from src.ui.widgets.dictionary_entry import DictionaryEntryView


class DictionaryScreen(MDScreen):
    """Screen with the searchable bilingual dictionary."""

    dictionary_service = None

    search_text = ""
    results = ListProperty([])

    def __init__(self, dictionary_service=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.dictionary_service = dictionary_service
        self.results = []
        self._build_ui()

    def _build_ui(self) -> None:
        root = BoxLayout(orientation="vertical")
        header = MDLabel(
            text="Dictionary",
            size_hint_y=None,
            height=dp(40),
            halign="center",
            valign="middle",
        )
        self.search_field = MDTextField(
            hint_text="Search a word or expression",
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
        self.results_container = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
        )
        root.add_widget(header)
        root.add_widget(search_row)
        root.add_widget(self.results_container)
        self.add_widget(root)

    def on_search(self, *args) -> None:
        """Run the dictionary search."""
        self.results = self.dictionary_service.search(
            self.search_text,
            source_language=None,
            target_language=None,
            limit=50,
        )
        self.results_container.clear_widgets()
        for entry in self.results:
            self.results_container.add_widget(DictionaryEntryView(entry))
