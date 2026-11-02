"""Main home screen of the MUTHU application."""

import threading

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

from src.config.settings import AppSettings
from src.core.language import KIMBUNDU, PORTUGUESE, get_language_name
from src.core.translation_result import TranslationResult
from src.core.validators import validate_translation_request
from src.services.storage_service import StorageService
from src.services.translation_service import TranslationService
from src.ui.widgets.buttons import create_mdbutton
from src.ui.widgets.language_selector import LanguageSelector
from src.ui.widgets.text_input import SourceTextInput
from src.ui.widgets.translation_card import TranslationCard

NAVIGATION_ROUTES = {
    "home": "Home",
    "dictionary": "Dictionary",
    "history": "History",
    "favorites": "Favorites",
    "settings": "Settings",
}


class HomeScreen(MDScreen):
    """Main screen: translation input, result and actions."""

    translation_service = ObjectProperty(None)
    storage_service = ObjectProperty(None)
    settings = ObjectProperty(None)

    source_language = StringProperty(PORTUGUESE)
    target_language = StringProperty(KIMBUNDU)
    source_text = StringProperty("")
    result = ObjectProperty(None)
    is_loading = BooleanProperty(False)
    status_message = StringProperty("")

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._build_ui()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _build_ui(self) -> None:
        root = BoxLayout(orientation="vertical", size_hint_y=1)

        header = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(90))
        title = MDLabel(
            text="MUTHU",
            size_hint_y=None,
            height=dp(40),
            halign="center",
            valign="middle",
        )
        subtitle = MDLabel(
            text="Two languages. One connection.",
            size_hint_y=None,
            height=dp(30),
            halign="center",
            valign="middle",
        )
        header.add_widget(title)
        header.add_widget(subtitle)

        content = BoxLayout(
            orientation="vertical",
            size_hint_y=1,
            padding=dp(12),
            spacing=dp(4),
        )

        self.language_selector = LanguageSelector(
            source_language=self.source_language,
            target_language=self.target_language,
        )
        self.language_selector.size_hint_y = 0
        self.language_selector.height = dp(56)
        self.language_selector.bind(
            source_language=self._on_source_language_change,
            target_language=self._on_target_language_change,
        )

        self.source_text_input = SourceTextInput(max_length=5000)
        self.source_text_input.size_hint_y = 0
        self.source_text_input.height = dp(110)
        self.source_text_input.bind(source_text=self._on_source_text_change)
        self.bind(status_message=self._on_status_message_change)

        self.translate_button = create_mdbutton(
            "Translate",
            on_release=self.on_translate,
            size_hint_x=None,
            width=dp(140),
            size_hint_y=0,
            height=dp(48),
        )
        self.copy_button = create_mdbutton(
            "Copy",
            on_release=self.on_copy,
            size_hint_x=None,
            width=dp(120),
            size_hint_y=0,
            height=dp(48),
        )
        self.clear_button = create_mdbutton(
            "Clear",
            on_release=self.on_clear,
            size_hint_x=None,
            width=dp(120),
            size_hint_y=0,
            height=dp(48),
        )
        self.save_button = create_mdbutton(
            "Save",
            on_release=self.on_save,
            size_hint_x=None,
            width=dp(100),
            size_hint_y=0,
            height=dp(48),
        )
        self.swap_button = MDIconButton(
            icon="swap-vertical",
            size_hint_x=None,
            width=dp(48),
            size_hint_y=0,
            height=dp(48),
            on_release=self.on_swap,
        )
        self.action_row = BoxLayout(orientation="horizontal", spacing=dp(8))
        self.action_row.size_hint_y = 0
        self.action_row.height = dp(40)
        self.action_row.add_widget(self.copy_button)
        self.action_row.add_widget(self.clear_button)
        self.action_row.add_widget(self.swap_button)
        self.action_row.add_widget(self.translate_button)
        self.action_row.add_widget(self.save_button)

        self.favorites_button = create_mdbutton(
            "Favorites",
            on_release=self.on_open_favorites,
            size_hint_x=None,
            width=dp(140),
            size_hint_y=0,
            height=dp(36),
        )

        self.result_card = TranslationCard(result=None)
        self.result_card.size_hint_y = 0
        self.result_card.height = dp(180)
        self.status_label = MDLabel(
            text="",
            size_hint_y=0,
            height=dp(20),
            halign="left",
            valign="middle",
        )

        content.add_widget(self.language_selector)
        content.add_widget(self.source_text_input)
        content.add_widget(self.favorites_button)
        content.add_widget(self.action_row)
        content.add_widget(self.status_label)
        content.add_widget(self.result_card)

        root.add_widget(header)
        root.add_widget(content)
        self.add_widget(root)

    # ------------------------------------------------------------------
    # Property handlers
    # ------------------------------------------------------------------
    def _on_source_language_change(self, instance, value) -> None:
        """Keep the source language in sync with the selector."""
        self.source_language = value

    def _on_target_language_change(self, instance, value) -> None:
        """Keep the target language in sync with the selector."""
        self.target_language = value

    def _on_source_text_change(self, instance, value) -> None:
        """Keep the source text in sync with the input widget."""
        self.source_text = value

    def _on_status_message_change(self, instance, value) -> None:
        """Keep the status label in sync with the status message."""
        self.status_label.text = value or ""

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def on_translate(self, *args) -> None:
        """Translate the current source text."""
        text = self.source_text.strip()
        error = validate_translation_request(
            text, self.source_language, self.target_language
        )
        if error is not None:
            self.status_message = error
            return
        self.is_loading = True
        self.status_message = "Translating..."
        self.result = None
        self._run_translation()

    def _run_translation(self, *args) -> None:
        """Run the translation workflow in the background."""

        def worker() -> None:
            result = self.translation_service.translate(
                self.source_text, self.source_language, self.target_language
            )
            Clock.schedule_once(lambda dt: self._apply_result(result), 0)

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()

    def _apply_result(self, result: TranslationResult) -> None:
        """Apply a translation result to the interface."""
        self.is_loading = False
        self.result = result
        if result.is_error:
            self.status_message = result.notes[0] if result.notes else "Translation failed."
        elif result.is_unsupported:
            self.status_message = result.notes[0] if result.notes else "Unsupported expression."
        elif result.is_success:
            self.status_message = "Translation ready."
        self.result_card.update(result)

    def on_copy(self, *args) -> None:
        """Copy the translated text to the clipboard."""
        if self.result is not None and self.result.is_success:
            from kivy.clipboard import Clipboard

            Clipboard.copy(self.result.translated_text)

    def on_swap(self, *args) -> None:
        """Swap the source and target languages."""
        source = self.source_language
        target = self.target_language
        self.language_selector.source_language = target
        self.language_selector.target_language = source

    def on_save(self, *args) -> None:
        """Save the current translation as a favorite."""
        if self.result is None or not self.result.is_success:
            return
        if self.storage_service is None:
            return
        self.storage_service.add_favorite(
            original_text=self.result.original_text,
            translated_text=self.result.translated_text,
            source_language=self.result.source_language,
            target_language=self.result.target_language,
        )

    def on_clear(self, *args) -> None:
        """Clear the source text and the translation result."""
        self.source_text_input.set("")
        self.source_text = ""
        self.result = None
        self.status_message = ""

    def on_open_favorites(self, *args) -> None:
        """Open the favorites screen."""
        if self.manager is not None:
            self.manager.current = "favorites"
