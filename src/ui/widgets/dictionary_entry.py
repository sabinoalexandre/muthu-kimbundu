"""Compact material card for a bilingual dictionary record."""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

from src.database.models import DictionaryEntry
from src.ui.widgets.theme import DARK_SURFACE, SURFACE, bind_theme_color


class DictionaryEntryView(MDCard):
    """Show the word pair, annotations and verification status."""

    def __init__(self, entry: DictionaryEntry, **kwargs) -> None:
        super().__init__(orientation="vertical", padding=dp(16), spacing=dp(6),
                         size_hint_y=None, radius=[dp(18)], elevation=0,
                         md_bg_color=(1, 1, 1, 1), **kwargs)
        bind_theme_color(self, "md_bg_color", SURFACE, DARK_SURFACE)
        self.entry = entry
        body = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(5))
        body.bind(minimum_height=body.setter("height"))
        self.height = dp(130)
        body.add_widget(MDLabel(text=entry.kimbundu_term, font_style="Title", role="medium", bold=True,
                                size_hint_y=None, height=dp(30), shorten=True))
        body.add_widget(MDLabel(text=entry.portuguese_translation, font_style="Body", role="large",
                                size_hint_y=None, height=dp(28), shorten=True))
        if entry.definition:
            body.add_widget(MDLabel(text=f"Definição · {entry.definition}", theme_text_color="Secondary",
                                    size_hint_y=None, height=dp(26), shorten=True))
        if entry.alternative_meanings:
            body.add_widget(MDLabel(text="Alternativas · " + ", ".join(entry.alternative_meanings),
                                    theme_text_color="Secondary", size_hint_y=None, height=dp(26), shorten=True))
        metadata = []
        if entry.grammatical_category:
            metadata.append(entry.grammatical_category)
        metadata.append("Verificada" if entry.verification_status == "verified" else "Não verificada")
        if entry.source_reference:
            metadata.append(entry.source_reference)
        body.add_widget(MDLabel(text=" · ".join(metadata), theme_text_color="Secondary",
                                font_style="Label", role="small", size_hint_y=None, height=dp(24), shorten=True))
        self.add_widget(body)
        self.bind(minimum_height=lambda *_: None)
        body.bind(height=self._fit_height)

    def _fit_height(self, _instance, value) -> None:
        self.height = value + dp(32)
