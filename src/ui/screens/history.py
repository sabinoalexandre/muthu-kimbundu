"""Translation history screen."""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField

from src.services.storage_service import StorageService


class HistoryScreen(MDScreen):
    """Browse, search and remove saved translation lookups."""

    storage_service = None

    def __init__(self, storage_service=None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.storage_service = storage_service
        self.entries = []
        self._build_ui()

    def _build_ui(self) -> None:
        root = BoxLayout(orientation="vertical", padding=[dp(20), dp(16)], spacing=dp(12))
        header = BoxLayout(size_hint_y=None, height=dp(44))
        header.add_widget(MDLabel(text="Histórico", font_style="Headline", role="small", bold=True))
        header.add_widget(MDIconButton(icon="delete-sweep-outline", on_release=self.on_clear_history))
        root.add_widget(header)
        self.search_field = MDTextField(hint_text="Pesquisar histórico", mode="outlined",
                                        size_hint_y=None, height=dp(56))
        self.search_field.bind(text=lambda *_: self._rebuild_rows())
        root.add_widget(self.search_field)
        self.count_label = MDLabel(text="As consultas ficam guardadas neste dispositivo.",
                                   theme_text_color="Secondary", size_hint_y=None, height=dp(30))
        root.add_widget(self.count_label)
        scroll = ScrollView(do_scroll_x=False, bar_width=dp(3))
        self.entries_container = BoxLayout(orientation="vertical", size_hint_y=None,
                                           spacing=dp(10), padding=[0, dp(4)])
        self.entries_container.bind(minimum_height=self.entries_container.setter("height"))
        scroll.add_widget(self.entries_container)
        root.add_widget(scroll)
        self.add_widget(root)

    def refresh(self) -> None:
        if self.storage_service is not None:
            self.entries = self.storage_service.get_history(limit=100)
        self._rebuild_rows()

    def _rebuild_rows(self, *args) -> None:
        if not hasattr(self, "entries_container"):
            return
        term = (self.search_field.text or "").strip().lower()
        entries = [item for item in self.entries if not term or term in item.original_text.lower()
                   or term in item.translated_text.lower() or term in (item.provider or "").lower()]
        self.entries_container.clear_widgets()
        self.count_label.text = f"{len(entries)} consulta(s) · resultados de dicionário"
        if not entries:
            self.entries_container.add_widget(MDLabel(
                text="Ainda não há consultas guardadas." if not term else "Nenhum registo corresponde à pesquisa.",
                theme_text_color="Secondary", size_hint_y=None, height=dp(72), halign="center"))
            return
        for entry in entries:
            card = MDCard(orientation="vertical", size_hint_y=None, height=dp(142),
                          padding=dp(14), spacing=dp(5), radius=[dp(16)])
            card.add_widget(MDLabel(text=entry.original_text, bold=True,
                                    size_hint_y=None, height=dp(28), shorten=True))
            card.add_widget(MDLabel(text=entry.translated_text, size_hint_y=None,
                                    height=dp(28), shorten=True))
            card.add_widget(MDLabel(
                text=f"{entry.source_language} → {entry.target_language} · {entry.verification_status} · {entry.timestamp}",
                theme_text_color="Secondary", font_style="Label", role="small", size_hint_y=None, height=dp(24)))
            actions = BoxLayout(size_hint_y=None, height=dp(34))
            actions.add_widget(MDLabel(text=entry.provider or "Consulta local", theme_text_color="Secondary"))
            delete = MDIconButton(icon="delete-outline", on_release=lambda *_args, item_id=entry.id: self.on_delete(item_id))
            actions.add_widget(delete)
            card.add_widget(actions)
            self.entries_container.add_widget(card)

    def on_delete(self, entry_id) -> None:
        if self.storage_service is not None and entry_id is not None:
            self.storage_service.delete_history(entry_id)
            self.refresh()

    def on_clear_history(self, *args) -> None:
        if self.storage_service is not None:
            self.storage_service.clear_history()
            self.refresh()
