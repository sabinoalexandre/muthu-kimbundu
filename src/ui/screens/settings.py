"""Application preferences and data management."""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

from src.services.storage_service import StorageService
from src.ui.widgets.buttons import create_mdbutton


class SettingsScreen(MDScreen):
    """Configure appearance and manage locally saved data."""

    storage_service = None
    settings = None

    def __init__(self, storage_service=None, settings=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.storage_service = storage_service
        self.settings = settings
        self._build_ui()

    def _build_ui(self) -> None:
        scroll = ScrollView(do_scroll_x=False, bar_width=dp(3))
        root = BoxLayout(orientation="vertical", size_hint_y=None,
                         padding=[dp(20), dp(16)], spacing=dp(14))
        root.bind(minimum_height=root.setter("height"))
        root.add_widget(MDLabel(text="Ajustes", font_style="Headline", role="small", bold=True,
                                size_hint_y=None, height=dp(42)))
        appearance = MDCard(orientation="vertical", padding=dp(16), spacing=dp(8),
                            size_hint_y=None, height=dp(156), radius=[dp(18)])
        appearance.add_widget(MDLabel(text="Aparência", font_style="Title", role="medium",
                                      size_hint_y=None, height=dp(30)))
        appearance.add_widget(MDLabel(text="Escolha o tema que prefere.", theme_text_color="Secondary",
                                      size_hint_y=None, height=dp(24)))
        theme_row = BoxLayout(spacing=dp(8))
        self.theme_light_button = create_mdbutton("Claro", on_release=self.on_theme_light, style="outlined", size_hint_x=1)
        self.theme_dark_button = create_mdbutton("Escuro", on_release=self.on_theme_dark, style="outlined", size_hint_x=1)
        theme_row.add_widget(self.theme_light_button)
        theme_row.add_widget(self.theme_dark_button)
        appearance.add_widget(theme_row)
        root.add_widget(appearance)

        data_card = MDCard(orientation="vertical", padding=dp(16), spacing=dp(8),
                           size_hint_y=None, height=dp(188), radius=[dp(18)])
        data_card.add_widget(MDLabel(text="Os seus dados", font_style="Title", role="medium",
                                     size_hint_y=None, height=dp(30)))
        data_card.add_widget(MDLabel(text="Limpe as consultas ou palavras guardadas neste dispositivo.",
                                     theme_text_color="Secondary", size_hint_y=None, height=dp(48)))
        self.clear_history_button = create_mdbutton("Limpar histórico", on_release=self.on_clear_history,
                                                       style="outlined", size_hint_x=1, size_hint_y=None, height=dp(42))
        self.clear_favorites_button = create_mdbutton("Limpar favoritos", on_release=self.on_clear_favorites,
                                                        style="outlined", size_hint_x=1, size_hint_y=None, height=dp(42))
        data_card.add_widget(self.clear_history_button)
        data_card.add_widget(self.clear_favorites_button)
        root.add_widget(data_card)

        info = MDCard(orientation="vertical", padding=dp(16), size_hint_y=None,
                      height=dp(128), radius=[dp(18)])
        info.add_widget(MDLabel(text="MUTHU", font_style="Title", role="medium", bold=True,
                                size_hint_y=None, height=dp(30)))
        info.add_widget(MDLabel(text="Duas línguas. Uma conexão.\nPortuguês ↔ Kimbundu",
                                theme_text_color="Secondary", size_hint_y=None, height=dp(52)))
        root.add_widget(info)
        root.add_widget(MDLabel(
            text="As consultas usam o dicionário local. Uma palavra encontrada não garante uma tradução contextual.",
            theme_text_color="Secondary", font_style="Body", role="small", size_hint_y=None, height=dp(58),
        ))
        scroll.add_widget(root)
        self.add_widget(scroll)

    def on_theme_light(self, *args) -> None:
        self._apply_theme("light")

    def on_theme_dark(self, *args) -> None:
        self._apply_theme("dark")

    def _apply_theme(self, theme: str) -> None:
        from kivy.app import App

        app = App.get_running_app()
        if app is not None and hasattr(app, "theme_cls"):
            app.theme_cls.theme_style = "Light" if theme == "light" else "Dark"
        if self.storage_service is not None:
            self.storage_service.save_preference("theme", theme)

    def on_clear_history(self, *args) -> None:
        if self.storage_service is not None:
            self.storage_service.clear_history()

    def on_clear_favorites(self, *args) -> None:
        if self.storage_service is not None:
            self.storage_service.clear_favorites()
