"""Translation result card widget."""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

from src.core.translation_result import TranslationResult, get_status_label


class TranslationCard(MDCard):
    """Card that displays a translation result and its reliability."""

    result = ObjectProperty(None)

    def __init__(self, result: TranslationResult = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.result = result
        self.radius = [dp(18)]
        self.elevation = 1
        self.headline = MDLabel(
            text="Resultado da consulta",
            size_hint_y=None,
            height=dp(30),
            halign="left",
            valign="middle",
        )
        self.translated_text_label = MDLabel(
            text="A tradução aparecerá aqui.",
            size_hint_y=None,
            height=dp(60),
            halign="left",
            valign="top",
            text_size=(dp(340), dp(100)),
        )
        self.status_label = MDLabel(
            text="",
            size_hint_y=None,
            height=dp(30),
            halign="left",
            valign="middle",
        )
        self.notes_label = MDLabel(
            text="",
            size_hint_y=None,
            height=dp(40),
            halign="left",
            valign="top",
            text_size=(dp(340), dp(80)),
        )
        inner = BoxLayout(orientation="vertical", size_hint_y=1, padding=dp(12), spacing=dp(4))
        inner.add_widget(self.headline)
        inner.add_widget(self.translated_text_label)
        inner.add_widget(self.status_label)
        inner.add_widget(self.notes_label)
        self.add_widget(inner)

    def update(self, result: TranslationResult) -> None:
        """Refresh the card contents from a translation result."""
        self.result = result
        self.translated_text_label.text = (
            result.translated_text if result and result.translated_text
            else "A tradução aparecerá aqui." if result is None else ""
        )
        self.headline.text = "Resultado da consulta"
        self.status_label.text = get_status_label(result.status) if result else "Aguardando consulta"
        if result and result.notes:
            self.notes_label.text = " · ".join(result.notes)
        elif result and not result.is_success:
            self.notes_label.text = result.original_text
        else:
            self.notes_label.text = ""
