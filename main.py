"""MUTHU application entry point."""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.card import MDCard

from src.config.settings import AppSettings
from src.core.language import KIMBUNDU, PORTUGUESE
from src.core.translator import Translator
from src.database import db
from src.providers.dictionary_provider import LocalDictionaryProvider
from src.services.dictionary_service import DictionaryService
from src.services.storage_service import StorageService
from src.services.translation_service import TranslationService
from src.ui.screens.dictionary import DictionaryScreen
from src.ui.screens.favorites import FavoritesScreen
from src.ui.screens.history import HistoryScreen
from src.ui.screens.home import HomeScreen
from src.ui.screens.settings import SettingsScreen

NAVIGATION_ITEMS = (
    ("Início", "home", "home-outline"),
    ("Léxico", "dictionary", "book-open-variant"),
    ("Hist.", "history", "history"),
    ("Salvos", "favorites", "heart-outline"),
    ("Ajustes", "settings", "cog-outline"),
)


class MuthuApp(MDApp):
    """MUTHU --- Portuguese <-> Kimbundu translation application."""

    def build(self):
        """Build the application navigation structure."""
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.primary_hue = "700"
        db.initialize_database()
        settings = AppSettings.from_env()
        dictionary_provider = LocalDictionaryProvider()
        translator = Translator(dictionary_provider)
        storage_service = StorageService()
        translation_service = TranslationService(translator, storage_service)
        dictionary_service = DictionaryService(dictionary_provider)

        self.settings = settings
        self.storage_service = storage_service
        self.translator = translator
        self.translation_service = translation_service
        self.dictionary_service = dictionary_service

        home_screen = HomeScreen(
            name="home",
            translation_service=translation_service,
            storage_service=storage_service,
            settings=settings,
        )
        dictionary_screen = DictionaryScreen(name="dictionary", dictionary_service=dictionary_service)
        history_screen = HistoryScreen(name="history", storage_service=storage_service)
        favorites_screen = FavoritesScreen(name="favorites", storage_service=storage_service)
        settings_screen = SettingsScreen(
            name="settings",
            storage_service=storage_service, settings=settings
        )

        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(home_screen)
        self.screen_manager.add_widget(dictionary_screen)
        self.screen_manager.add_widget(history_screen)
        self.screen_manager.add_widget(favorites_screen)
        self.screen_manager.add_widget(settings_screen)

        shell = BoxLayout(orientation="vertical")
        shell.add_widget(self.screen_manager)
        self.navigation_bar = MDCard(
            size_hint_y=None, height=dp(72), radius=[dp(20), dp(20), 0, 0],
            elevation=2, padding=[dp(4), dp(4)],
        )
        nav_row = BoxLayout(spacing=dp(2))
        self.navigation_buttons = {}
        for title, route, icon in NAVIGATION_ITEMS:
            button = MDButton(style="text", size_hint_x=1)
            button.add_widget(MDButtonText(text=title))
            button.bind(on_release=lambda instance, route=route: self._on_drawer_item_release(route))
            self.navigation_buttons[route] = button
            nav_row.add_widget(button)
        self.navigation_bar.add_widget(nav_row)
        shell.add_widget(self.navigation_bar)
        self.screen_manager.bind(current=self._on_screen_change)
        self._on_screen_change(self.screen_manager, self.screen_manager.current)
        return shell

    def _on_screen_change(self, instance, route: str) -> None:
        """Refresh list views whenever their navigation tab is opened."""
        for key, button in self.navigation_buttons.items():
            button.style = "filled" if key == route else "text"
        screen = self.screen_manager.get_screen(route)
        if hasattr(screen, "refresh"):
            screen.refresh()

    def _on_drawer_item_release(self, route: str) -> None:
        """Open the requested screen from the navigation drawer."""
        self.screen_manager.current = route

    def on_start(self) -> None:
        """Apply the persisted theme when the application starts."""
        theme = "light"
        if self.storage_service is not None:
            theme = self.storage_service.get_preference("theme", "light") or "light"
        self.theme_cls.theme_style = "Light" if theme == "light" else "Dark"


if __name__ == "__main__":
    MuthuApp().run()
