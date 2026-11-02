"""Source and target language selector widget."""

from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDIconButton
from kivymd.uix.dialog import MDDialog, MDDialogContentContainer, MDDialogHeadlineText

from src.core.language import SUPPORTED_LANGUAGES, get_language_name
from src.ui.widgets.buttons import create_mdbutton


def _language_label(code: str) -> str:
    return {"pt": "Português", "kimbundu": "Kimbundu"}.get(code, get_language_name(code))


class LanguageSelector(BoxLayout):
    """Widget with source and target language selectors."""

    source_language = StringProperty("pt")
    target_language = StringProperty("kimbundu")

    def __init__(
        self,
        source_language: str = "pt",
        target_language: str = "kimbundu",
        on_swap=None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.spacing = dp(7)
        self.on_swap = on_swap
        self.source_button = create_mdbutton(
            _language_label(source_language),
            on_release=self.open_source_dialog,
            size_hint_x=1,
            style="tonal",
        )
        self.target_button = create_mdbutton(
            _language_label(target_language),
            on_release=self.open_target_dialog,
            size_hint_x=1,
            style="tonal",
        )
        self.swap_button = MDIconButton(
            icon="swap-horizontal", on_release=self._swap,
            size_hint=(None, 1), width=dp(42),
        )
        self.source_button_text = self.source_button.children[0]
        self.target_button_text = self.target_button.children[0]
        self.bind(source_language=self._update_source_label, target_language=self._update_target_label)
        self.add_widget(self.source_button)
        self.add_widget(self.swap_button)
        self.add_widget(self.target_button)
        self.dialog = None

    def _swap(self, *_args) -> None:
        if self.on_swap is not None:
            self.on_swap()

    def open_source_dialog(self, *args) -> None:
        """Open the source language dialog."""
        self._open_dialog("Source")

    def open_target_dialog(self, *args) -> None:
        """Open the target language dialog."""
        self._open_dialog("Target")

    def _update_source_label(self, _instance, code: str) -> None:
        self.source_button_text.text = _language_label(code)

    def _update_target_label(self, _instance, code: str) -> None:
        self.target_button_text.text = _language_label(code)

    def _open_dialog(self, action: str) -> None:
        """Open a modal dialog listing the supported languages."""
        content = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(200))
        for code in SUPPORTED_LANGUAGES:
            button = create_mdbutton(
                _language_label(code),
                on_release=lambda _button, code=code: self._select_language(code, action),
                size_hint_y=None,
                height=dp(48),
            )
            content.add_widget(button)
        content.bind(minimum_height=content.setter("height"))
        scroll = ScrollView(size_hint=(1, None), height=dp(200), do_scroll_x=False)
        scroll.add_widget(content)
        self.dialog = MDDialog()
        self.dialog.add_widget(MDDialogHeadlineText(
            text="Escolha o idioma de origem" if action == "Source" else "Escolha o idioma de destino",
        ))
        self.dialog.add_widget(MDDialogContentContainer(scroll))
        self.dialog.open()

    def _select_language(self, code: str, action: str) -> None:
        """Persist the language selection and close the dialog."""
        if action == "Source":
            previous_source = self.source_language
            self.source_language = code
            if code == self.target_language:
                self.target_language = previous_source
        else:
            previous_target = self.target_language
            self.target_language = code
            if code == self.source_language:
                self.source_language = previous_target
        if self.dialog is not None:
            self.dialog.dismiss()
            self.dialog = None
