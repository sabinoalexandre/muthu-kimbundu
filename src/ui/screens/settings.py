"""Settings screen."""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

from src.config.settings import AppSettings
from src.services.storage_service import StorageService
from src.ui.widgets.buttons import create_mdbutton


class SettingsScreen(MDScreen):
    """Screen with application settings and data management."""

    storage_service = None
    settings = None

    def __init__(self, storage_service=None, settings=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.storage_service = storage_service
        self.settings = settings
        self._build_ui()

    def _build_ui(self) -> None:
        root = BoxLayout(orientation="vertical")
        header = MDLabel(
            text="Settings",
            size_hint_y=None,
            height=dp(40),
            halign="center",
            valign="middle",
        )
        self.theme_light_button = create_mdbutton(
            "Light theme",
            on_release=self.on_theme_light,
            size_hint_x=None,
            width=dp(160),
        )
        self.theme_dark_button = create_mdbutton(
            "Dark theme",
            on_release=self.on_theme_dark,
            size_hint_x=None,
            width=dp(160),
        )
        self.clear_history_button = create_mdbutton(
            "Clear history",
            on_release=self.on_clear_history,
            size_hint_x=None,
            width=dp(180),
        )
        self.clear_favorites_button = create_mdbutton(
            "Clear favorites",
            on_release=self.on_clear_favorites,
            size_hint_x=None,
            width=dp(180),
        )
        info = MDLabel(
            text="MUTHU --- Portuguese <-> Kimbundu translator.",
            size_hint_y=None,
            height=dp(60),
            halign="center",
            valign="middle",
        )
        root.add_widget(header)
        root.add_widget(self.theme_light_button)
        root.add_widget(self.theme_dark_button)
        root.add_widget(self.clear_history_button)
        root.add_widget(self.clear_favorites_button)
        root.add_widget(info)
        self.add_widget(root)

    def on_theme_light(self, *args) -> None:
        """Switch to the light theme."""
        self._apply_theme("light")

    def on_theme_dark(self, *args) -> None:
        """Switch to the dark theme."""
        self._apply_theme("dark")

    def _apply_theme(self, theme: str) -> None:
        """Apply and persist the selected theme."""
        from kivy.app import App

        app = App.get_running_app()
        if app is not None and hasattr(app, "theme_cls"):
            app.theme_cls.theme_style = "Light" if theme == "light" else "Dark"
        if self.storage_service is not None:
            self.storage_service.save_preference("theme", theme)

    def on_clear_history(self, *args) -> None:
        """Clear the translation history."""
        if self.storage_service is None:
            return
        self.storage_service.clear_history()

    def on_clear_favorites(self, *args) -> None:
        """Clear all favorites."""
        if self.storage_service is None:
            return
        self.storage_service.clear_favorites()
