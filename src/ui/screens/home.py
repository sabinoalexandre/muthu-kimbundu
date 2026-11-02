"""Main home screen of the MUTHU application."""

import threading

from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDIcon, MDLabel
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
from src.ui.widgets.theme import ACCENT_BLUE, apply_page_background

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
    result = ObjectProperty(None, allownone=True)
    is_loading = BooleanProperty(False)
    status_message = StringProperty("")

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._translation_request = 0
        self._build_ui()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _build_ui(self) -> None:
        root = BoxLayout(orientation="vertical", size_hint_y=1)
        apply_page_background(root)
        scroll = ScrollView(do_scroll_x=False, bar_width=dp(3))
        content = BoxLayout(orientation="vertical", size_hint_y=None, padding=[dp(18), dp(12)], spacing=dp(13))
        content.bind(minimum_height=content.setter("height"))

        header = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(62), spacing=dp(12))
        brand_mark = MDCard(size_hint=(None, None), size=(dp(52), dp(52)), radius=[dp(18)],
                            md_bg_color=ACCENT_BLUE, elevation=0)
        brand_mark.add_widget(MDIcon(icon="translate", halign="center", theme_text_color="Custom",
                                     text_color=(1, 1, 1, 1)))
        header.add_widget(brand_mark)
        brand_text = BoxLayout(orientation="vertical", spacing=dp(1))
        title = MDLabel(
            text="MUTHU",
            font_style="Headline", role="small", bold=True,
            size_hint_y=None, height=dp(34), halign="left", valign="middle",
        )
        subtitle = MDLabel(
            text="Duas línguas. Uma conexão.",
            size_hint_y=None, height=dp(21), halign="left", valign="middle",
            theme_text_color="Secondary",
        )
        brand_text.add_widget(title)
        brand_text.add_widget(subtitle)
        header.add_widget(brand_text)

        hero = MDCard(orientation="vertical", size_hint_y=None, height=dp(116), padding=dp(18),
                      spacing=dp(5), radius=[dp(22)], elevation=0,
                      md_bg_color=ACCENT_BLUE)
        hero.add_widget(MDLabel(text="PORTUGUÊS  ·  KIMBUNDU", font_style="Label", role="small",
                                theme_text_color="Custom", text_color=(0.78, 0.88, 1.0, 1),
                                size_hint_y=None, height=dp(20)))
        hero.add_widget(MDLabel(text="Palavras que criam pontes.", font_style="Headline",
                                role="small", bold=True, theme_text_color="Custom",
                                text_color=(1, 1, 1, 1), size_hint_y=None, height=dp(34)))
        hero.add_widget(MDLabel(text="Uma consulta de cada vez, com respeito pela língua.",
                                theme_text_color="Custom", text_color=(0.88, 0.94, 1.0, 1),
                                size_hint_y=None, height=dp(24)))

        self.language_selector = LanguageSelector(
            source_language=self.source_language,
            target_language=self.target_language,
            on_swap=self.on_swap,
        )
        self.language_selector.size_hint_y = None
        self.language_selector.height = dp(58)
        self.language_selector.bind(
            source_language=self._on_source_language_change,
            target_language=self._on_target_language_change,
        )

        self.source_text_input = SourceTextInput(max_length=5000)
        self.source_text_input.size_hint_y = None
        self.source_text_input.height = dp(122)
        self.source_text_input.bind(source_text=self._on_source_text_change)
        self.bind(status_message=self._on_status_message_change)
        self.bind(is_loading=self._on_loading_change)

        self.translate_button = create_mdbutton(
            "Traduzir",
            on_release=self.on_translate,
            style="filled", size_hint_x=1,
            size_hint_y=None, height=dp(54),
        )
        self.copy_button = create_mdbutton(
            "Copiar",
            on_release=self.on_copy,
            style="outlined", size_hint_x=1,
            size_hint_y=None, height=dp(40),
        )
        self.clear_button = create_mdbutton(
            "Limpar",
            on_release=self.on_clear,
            style="outlined", size_hint_x=1,
            size_hint_y=None, height=dp(40),
        )
        self.save_button = create_mdbutton(
            "Guardar",
            on_release=self.on_save,
            style="outlined", size_hint_x=1,
            size_hint_y=None, height=dp(40),
        )
        self.secondary_actions = BoxLayout(
            orientation="horizontal", spacing=dp(8), size_hint_y=None, height=dp(52),
        )
        for button in (self.copy_button, self.clear_button, self.save_button):
            button.height = dp(48)
            self.secondary_actions.add_widget(button)

        self.result_card = TranslationCard(result=None)
        self.result_card.size_hint_y = None
        self.result_card.height = dp(194)
        self.status_label = MDLabel(
            text="",
            size_hint_y=None, height=0, halign="left",
            valign="middle",
            theme_text_color="Secondary", font_style="Body", role="small",
        )

        content.add_widget(header)
        content.add_widget(hero)
        pair_card = MDCard(size_hint_y=None, height=dp(70), padding=[dp(6), dp(5)],
                           radius=[dp(19)], elevation=0, md_bg_color=(1, 1, 1, 1))
        pair_card.add_widget(self.language_selector)
        content.add_widget(pair_card)
        content.add_widget(MDLabel(text="A SUA MENSAGEM", font_style="Label", role="small",
                                   theme_text_color="Secondary", size_hint_y=None, height=dp(18)))
        input_card = MDCard(orientation="vertical", padding=dp(9), size_hint_y=None,
                            height=dp(142), radius=[dp(20)], elevation=0,
                            md_bg_color=(1, 1, 1, 1))
        input_card.add_widget(self.source_text_input)
        content.add_widget(input_card)
        content.add_widget(self.translate_button)
        content.add_widget(self.secondary_actions)
        content.add_widget(self.status_label)
        content.add_widget(MDLabel(text="RESULTADO", font_style="Label", role="small",
                                   theme_text_color="Secondary", size_hint_y=None, height=dp(18)))
        content.add_widget(self.result_card)
        scroll.add_widget(content)
        root.add_widget(scroll)
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
        self.status_label.height = dp(22) if value else 0

    def _on_loading_change(self, _instance, value: bool) -> None:
        self.translate_button.disabled = value
        self.translate_button.children[0].text = "A consultar…" if value else "Traduzir"

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------
    def on_translate(self, *args) -> None:
        """Translate the current source text."""
        if self.is_loading:
            return
        text = self.source_text.strip()
        error = validate_translation_request(
            text, self.source_language, self.target_language
        )
        if error is not None:
            self.status_message = error
            return
        self.is_loading = True
        self.status_message = "A consultar o dicionário…"
        self.result = None
        self.result_card.update(None)
        self._translation_request += 1
        self._run_translation(text, self.source_language, self.target_language, self._translation_request)

    def _run_translation(self, text: str, source: str, target: str, request_id: int) -> None:
        """Run the translation workflow in the background."""

        def worker() -> None:
            try:
                result = self.translation_service.translate(text, source, target)
            except Exception as exc:  # noqa: BLE001 - always release the loading state
                result = TranslationResult.error(
                    text, source, target, f"Falha inesperada na consulta: {exc}",
                    method="LocalDictionaryProvider",
                )
            Clock.schedule_once(lambda _dt: self._apply_result(result, request_id), 0)

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()

    def _apply_result(self, result: TranslationResult, request_id: int = None) -> None:
        """Apply a translation result to the interface."""
        if request_id is not None and request_id != self._translation_request:
            return
        self.is_loading = False
        self.result = result
        if result.is_error:
            self.status_message = result.notes[0] if result.notes else "Não foi possível concluir a consulta."
        elif result.is_unsupported:
            self.status_message = ""
        elif result.is_success:
            self.status_message = ""
        self.result_card.update(result)

    def on_copy(self, *args) -> None:
        """Copy the translated text to the clipboard."""
        if self.result is not None and self.result.translated_text:
            from kivy.core.clipboard import Clipboard

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
        self._translation_request += 1
        self.is_loading = False
        self.source_text_input.set("")
        self.source_text = ""
        self.result = None
        self.result_card.update(None)
        self.status_message = ""

    def on_open_favorites(self, *args) -> None:
        """Open the favorites screen."""
        if self.manager is not None:
            self.manager.current = "favorites"
