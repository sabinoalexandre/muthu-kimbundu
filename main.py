"""MUTHU application entry point."""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.navigationdrawer import (
    MDNavigationDrawer,
    MDNavigationDrawerItem,
    MDNavigationDrawerItemText,
    MDNavigationDrawerMenu,
    MDNavigationLayout,
)

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
    ("Home", "home"),
    ("Dictionary", "dictionary"),
    ("History", "history"),
    ("Favorites", "favorites"),
    ("Settings", "settings"),
)


class MuthuApp(MDApp):
    """MUTHU --- Portuguese <-> Kimbundu translation application."""

    def build(self):
        """Build the application navigation structure."""
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
            translation_service=translation_service,
            storage_service=storage_service,
            settings=settings,
        )
        dictionary_screen = DictionaryScreen(dictionary_service=dictionary_service)
        history_screen = HistoryScreen(storage_service=storage_service)
        favorites_screen = FavoritesScreen(storage_service=storage_service)
        settings_screen = SettingsScreen(
            storage_service=storage_service, settings=settings
        )

        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(home_screen)
        self.screen_manager.add_widget(dictionary_screen)
        self.screen_manager.add_widget(history_screen)
        self.screen_manager.add_widget(favorites_screen)
        self.screen_manager.add_widget(settings_screen)

        self.navigation_drawer = MDNavigationDrawer()
        self.navigation_drawer.add_widget(self._build_drawer_menu())
        self.navigation_drawer.drawer_type = "standard"
        self.navigation_drawer.anchor = "left"

        self.navigation_layout = MDNavigationLayout()
        self.navigation_layout._screen_manager = self.screen_manager
        self.navigation_layout._navigation_drawer = self.navigation_drawer
        self.navigation_layout.add_widget(self.navigation_drawer)
        self.navigation_layout.add_widget(self.screen_manager)
        return self.navigation_layout

    def _build_drawer_menu(self):
        """Build the navigation drawer menu with the application sections."""
        menu = MDNavigationDrawerMenu()
        for title, route in NAVIGATION_ITEMS:
            item = MDNavigationDrawerItem()
            item.add_widget(MDNavigationDrawerItemText(text=title))
            item.bind(on_release=lambda instance, route=route: self._on_drawer_item_release(route))
            menu.add_widget(item)
        return menu

    def _on_drawer_item_release(self, route: str) -> None:
        """Open the requested screen from the navigation drawer."""
        self.screen_manager.current = route
        if self.navigation_drawer is not None:
            self.navigation_drawer.set_state("close")

    def on_start(self) -> None:
        """Apply the persisted theme when the application starts."""
        theme = "light"
        if self.storage_service is not None:
            theme = self.storage_service.get_preference("theme", "light") or "light"
        self.theme_cls.theme_style = "Light" if theme == "light" else "Dark"


if __name__ == "__main__":
    MuthuApp().run()
