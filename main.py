"""MUTHU application entry point."""

from kivy.metrics import dp
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDIcon, MDLabel

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
    ("Início", "home", "home-variant"),
    ("Dicionário", "dictionary", "book-open-variant"),
    ("Histórico", "history", "history"),
    ("Favoritos", "favorites", "heart-outline"),
    ("Ajustes", "settings", "cog-outline"),
)


class NavigationItem(ButtonBehavior, BoxLayout):
    """Compact icon and label tab for the mobile navigation bar."""

    def __init__(self, title: str, icon: str, route: str, **kwargs):
        super().__init__(orientation="vertical", spacing=dp(2), padding=[dp(2), dp(5)], **kwargs)
        self.route = route
        self.active = False
        self.icon_label = MDIcon(icon=icon, halign="center", size_hint_y=None, height=dp(25))
        self.text_label = MDLabel(text=title, halign="center", font_style="Label",
                                  role="small", size_hint_y=None, height=dp(18), shorten=True)
        self.add_widget(self.icon_label)
        self.add_widget(self.text_label)
        with self.canvas.before:
            self._bg_color = Color(0, 0, 0, 0)
            self._bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(16)])
        self.bind(pos=self._sync_bg, size=self._sync_bg)

    def _sync_bg(self, *_args):
        self._bg.pos = self.pos
        self._bg.size = self.size

    def set_active(self, active: bool) -> None:
        self.active = active
        self._bg_color.rgba = (0.88, 0.94, 1.0, 1) if active else (0, 0, 0, 0)
        color = (0.10, 0.42, 0.70, 1) if active else (0.36, 0.45, 0.55, 1)
        self.icon_label.text_color = color
        self.text_label.text_color = color


class MuthuApp(MDApp):
    """MUTHU --- Portuguese <-> Kimbundu translation application."""

    def build(self):
        """Build the application navigation structure."""
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "700"
        self.theme_cls.theme_style = "Light"
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
            size_hint_y=None, height=dp(76), radius=[dp(22), dp(22), 0, 0],
            elevation=2, padding=[dp(8), dp(6)], md_bg_color=(1, 1, 1, 1),
        )
        nav_row = BoxLayout(spacing=dp(3))
        self.navigation_buttons = {}
        for title, route, icon in NAVIGATION_ITEMS:
            button = NavigationItem(title, icon, route, size_hint_x=1)
            button.bind(on_release=lambda _button, route=route: self._on_navigation(route))
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
            button.set_active(key == route)
        screen = self.screen_manager.get_screen(route)
        if hasattr(screen, "refresh"):
            screen.refresh()

    def _on_navigation(self, route: str) -> None:
        """Open a section from the mobile navigation bar."""
        self.screen_manager.current = route

    def on_start(self) -> None:
        """Apply the persisted theme when the application starts."""
        Window.softinput_mode = "below_target"
        theme = "light"
        if self.storage_service is not None:
            theme = self.storage_service.get_preference("theme", "light") or "light"
        self.theme_cls.theme_style = "Light" if theme == "light" else "Dark"


if __name__ == "__main__":
    MuthuApp().run()
