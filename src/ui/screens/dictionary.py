"""Bilingual dictionary screen."""

from kivy.metrics import dp
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField

from src.core.language import KIMBUNDU, PORTUGUESE
from src.services.dictionary_service import DictionaryService
from src.ui.widgets.dictionary_entry import DictionaryEntryView


class DictionaryScreen(MDScreen):
    """Search the local Portuguese–Kimbundu vocabulary."""

    dictionary_service = None
    results = ListProperty([])

    def __init__(self, dictionary_service=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.dictionary_service = dictionary_service
        self._build_ui()

    def _build_ui(self) -> None:
        root = BoxLayout(orientation="vertical", padding=[dp(20), dp(16)], spacing=dp(14))
        root.add_widget(MDLabel(
            text="Dicionário", font_style="Headline", role="small", bold=True,
            size_hint_y=None, height=dp(42),
        ))
        root.add_widget(MDLabel(
            text="Explore palavras e expressões nas duas línguas.",
            theme_text_color="Secondary", size_hint_y=None, height=dp(28),
        ))

        self.search_field = MDTextField(
            hint_text="Pesquisar palavra ou expressão", mode="outlined",
            size_hint_y=None, height=dp(56),
        )
        self.search_field.bind(text=self._on_search_text)
        root.add_widget(self.search_field)
        self.direction_label = MDLabel(
            text="Português ↔ Kimbundu · resultados do dicionário local",
            theme_text_color="Secondary", size_hint_y=None, height=dp(36),
        )
        root.add_widget(self.direction_label)

        scroll = ScrollView(do_scroll_x=False, bar_width=dp(3))
        self.results_container = BoxLayout(
            orientation="vertical", size_hint_y=None, spacing=dp(10), padding=[0, dp(4)],
        )
        self.results_container.bind(minimum_height=self.results_container.setter("height"))
        scroll.add_widget(self.results_container)
        root.add_widget(scroll)
        self.add_widget(root)

    def _on_search_text(self, instance, value) -> None:
        self.search_text = value
        self.on_search()

    def on_search(self, *args) -> None:
        """Search the dictionary in either language."""
        if self.dictionary_service is None:
            return
        self.results = self.dictionary_service.search(
            getattr(self, "search_text", ""), source_language=None,
            target_language=None, limit=50,
        )
        self.results_container.clear_widgets()
        if not self.results:
            query = getattr(self, "search_text", "").strip()
            message = "Nenhuma entrada encontrada." if query else "Comece por pesquisar uma palavra."
            self.results_container.add_widget(MDLabel(
                text=message, theme_text_color="Secondary",
                size_hint_y=None, height=dp(72), halign="center",
            ))
            return
        for entry in self.results:
            self.results_container.add_widget(DictionaryEntryView(entry))
