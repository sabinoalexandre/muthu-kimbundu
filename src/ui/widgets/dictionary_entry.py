"""Dictionary entry display widget."""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel

from src.database.models import DictionaryEntry


class DictionaryEntryView(BoxLayout):
    """Vertical display of a single bilingual dictionary entry."""

    def __init__(self, entry: DictionaryEntry, **kwargs) -> None:
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = dp(4)
        self.add_widget(MDLabel(text=entry.kimbundu_term, size_hint_y=None, height=dp(24), halign="left", valign="middle"))
        self.add_widget(MDLabel(text=entry.portuguese_translation, size_hint_y=None, height=dp(24), halign="left", valign="middle"))
        if entry.definition:
            self.add_widget(MDLabel(text=f"Definition: {entry.definition}", size_hint_y=None, height=dp(24), halign="left", valign="middle"))
        if entry.alternative_meanings:
            self.add_widget(MDLabel(text="Alternatives: " + ", ".join(entry.alternative_meanings), size_hint_y=None, height=dp(24), halign="left", valign="middle"))
        if entry.examples:
            self.add_widget(MDLabel(text="Examples: " + "; ".join(entry.examples), size_hint_y=None, height=dp(24), halign="left", valign="middle"))
        self.add_widget(MDLabel(text=f"Category: {entry.grammatical_category}", size_hint_y=None, height=dp(24), halign="left", valign="middle"))
        self.add_widget(MDLabel(text=f"Status: {entry.verification_status}", size_hint_y=None, height=dp(24), halign="left", valign="middle"))
        if entry.source_reference:
            self.add_widget(MDLabel(text=f"Source: {entry.source_reference}", size_hint_y=None, height=dp(24), halign="left", valign="middle"))
