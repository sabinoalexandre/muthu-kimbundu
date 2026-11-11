"""Translation result card widget."""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

from src.core.translation_result import TranslationResult, get_status_label


class TranslationCard(MDCard):
    """Card that displays a translation result and its reliability."""

    result = ObjectProperty(None, allownone=True)

    def __init__(self, result: TranslationResult = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.result = result
        self.radius = [dp(18)]
        self.elevation = 1
        self.translated_text_label = MDLabel(
            text="",
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
            height=0,
            halign="left",
            valign="top",
            text_size=(dp(340), dp(80)),
        )
        inner = BoxLayout(orientation="vertical", size_hint_y=1, padding=dp(12), spacing=dp(4))
        inner.add_widget(self.translated_text_label)
        inner.add_widget(self.status_label)
        inner.add_widget(self.notes_label)
        self.add_widget(inner)

    def update(self, result: TranslationResult) -> None:
        """Refresh the card contents from a translation result."""
        self.result = result
        self.translated_text_label.text = (
            result.translated_text if result and result.translated_text
            else ""
        )
        self.status_label.text = get_status_label(result.status) if result else "Aguardando consulta"
        if result is None:
            self.status_label.text = ""
            self.notes_label.text = ""
        elif result.is_unsupported:
            self.status_label.text = ""
            self.notes_label.text = ""
        elif result.is_success:
            self.status_label.text = (
                "Tradução verificada"
                if result.is_verified
                else "Correspondência de dicionário"
            )
            self.notes_label.text = ""
        elif result.is_error:
            self.status_label.text = "Não foi possível concluir a consulta"
            self.notes_label.text = ""
        else:
            self.notes_label.text = ""
