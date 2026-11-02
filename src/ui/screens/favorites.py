"""Saved translations screen."""

from kivy.core.clipboard import Clipboard
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField

from src.services.storage_service import StorageService
from src.ui.widgets.theme import ACCENT_BLUE, apply_page_background


class FavoritesScreen(MDScreen):
    """Find, copy and remove favorite expressions."""

    storage_service = None

    def __init__(self, storage_service=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.storage_service = storage_service
        self.favorites = []
        self._build_ui()

    def _build_ui(self) -> None:
        root = BoxLayout(orientation="vertical", padding=[dp(20), dp(16)], spacing=dp(12))
        apply_page_background(root)
        hero = MDCard(orientation="vertical", size_hint_y=None, height=dp(100), padding=dp(16),
                      spacing=dp(4), radius=[dp(22)], elevation=0, md_bg_color=ACCENT_BLUE)
        hero.add_widget(MDLabel(text="A SUA COLEÇÃO", font_style="Label", role="small",
                                theme_text_color="Custom", text_color=(0.80, 0.90, 1.0, 1),
                                size_hint_y=None, height=dp(20)))
        hero.add_widget(MDLabel(text="Favoritos", font_style="Headline", role="small", bold=True,
                                theme_text_color="Custom", text_color=(1, 1, 1, 1),
                                size_hint_y=None, height=dp(38)))
        root.add_widget(hero)
        search_card = MDCard(padding=[dp(12), dp(6)], size_hint_y=None, height=dp(70),
                             radius=[dp(19)], elevation=0, md_bg_color=(1, 1, 1, 1))
        self.search_field = MDTextField(hint_text="Pesquisar palavras guardadas", mode="outlined",
                                        size_hint_y=None, height=dp(56))
        self.search_field.bind(text=lambda *_: self._rebuild_rows())
        search_card.add_widget(self.search_field)
        root.add_widget(search_card)
        self.count_label = MDLabel(text="As suas palavras favoritas.", theme_text_color="Secondary",
                                   font_style="Label", role="small", size_hint_y=None, height=dp(24))
        root.add_widget(self.count_label)
        scroll = ScrollView(do_scroll_x=False, bar_width=dp(3))
        self.entries_container = BoxLayout(orientation="vertical", size_hint_y=None,
                                           spacing=dp(10), padding=[0, dp(4)])
        self.entries_container.bind(minimum_height=self.entries_container.setter("height"))
        scroll.add_widget(self.entries_container)
        root.add_widget(scroll)
        self.add_widget(root)

    def refresh(self) -> None:
        self.favorites = self.storage_service.get_favorites() if self.storage_service else []
        self._rebuild_rows()

    def _rebuild_rows(self, *args) -> None:
        if not hasattr(self, "entries_container"):
            return
        term = (self.search_field.text or "").strip().lower()
        visible = [fav for fav in self.favorites if not term or term in fav.original_text.lower()
                   or term in fav.translated_text.lower()]
        self.entries_container.clear_widgets()
        self.count_label.text = f"{len(visible)} expressão(ões) guardada(s)"
        if not visible:
            message = "Ainda não guardou nenhuma tradução." if not term else "Nenhum favorito corresponde à pesquisa."
            self.entries_container.add_widget(MDLabel(text=message, theme_text_color="Secondary",
                                                      size_hint_y=None, height=dp(72), halign="center"))
            return
        for favorite in visible:
            card = MDCard(orientation="vertical", size_hint_y=None, height=dp(112),
                          padding=dp(14), spacing=dp(5), radius=[dp(19)], elevation=0,
                          md_bg_color=(1, 1, 1, 1))
            card.add_widget(MDLabel(text=favorite.original_text, bold=True,
                                    size_hint_y=None, height=dp(28), shorten=True))
            card.add_widget(MDLabel(text=favorite.translated_text, size_hint_y=None,
                                    height=dp(26), shorten=True))
            actions = BoxLayout(size_hint_y=None, height=dp(34))
            actions.add_widget(MDLabel(text=f"{favorite.source_language} → {favorite.target_language}",
                                       theme_text_color="Secondary", font_style="Label", role="small"))
            actions.add_widget(MDIconButton(icon="content-copy", on_release=lambda *_args, item=favorite: self.on_copy(item)))
            actions.add_widget(MDIconButton(icon="heart-off-outline", on_release=lambda *_args, item_id=favorite.id: self.on_remove(item_id)))
            card.add_widget(actions)
            self.entries_container.add_widget(card)

    def on_copy(self, favorite) -> None:
        Clipboard.copy(favorite.translated_text)

    def on_remove(self, favorite_id) -> None:
        if self.storage_service is not None and favorite_id is not None:
            self.storage_service.remove_favorite(favorite_id)
            self.refresh()

    def on_clear(self, *args) -> None:
        if self.storage_service is not None:
            self.storage_service.clear_favorites()
            self.refresh()
