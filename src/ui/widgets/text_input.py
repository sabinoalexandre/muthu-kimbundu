"""Multi-line text input widget with character counter."""

from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput as KivyTextInput
from kivymd.uix.label import MDLabel


class SourceTextInput(BoxLayout):
    """Multi-line source text input area with a character counter."""

    source_text = StringProperty("")
    max_length = NumericProperty(5000)

    def __init__(self, max_length: int = 5000, **kwargs) -> None:
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = dp(4)
        self.padding = [dp(12), dp(10), dp(12), dp(6)]
        self.max_length = max_length
        with self.canvas.before:
            Color(0.945, 0.973, 0.996, 1)  # #F1F8FE
            self._background = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(18)])
        self.bind(pos=self._sync_background, size=self._sync_background)
        self.text_input = KivyTextInput(
            multiline=True,
            font_size="16sp",
            padding=[dp(4), dp(6), dp(4), dp(6)],
            background_color=(0, 0, 0, 0),
            foreground_color=(0.12, 0.17, 0.17, 1),
            cursor_color=(0.008, 0.467, 0.741, 1),
            hint_text="Escreva uma palavra ou expressão…",
        )
        self.counter = MDLabel(
            text="0 / 5000",
            size_hint_y=None,
            height=dp(18),
            halign="right",
            valign="middle",
            theme_text_color="Secondary",
            font_style="Label",
            role="small",
        )
        self.add_widget(self.text_input)
        self.add_widget(self.counter)
        self.bind(source_text=self._update_counter, max_length=self._update_counter)
        self.text_input.bind(text=self._on_text)

    def _sync_background(self, *_args) -> None:
        self._background.pos = self.pos
        self._background.size = self.size

    def _on_text(self, instance, value) -> None:
        """Keep the bound property and the character counter in sync."""
        self.source_text = value
        self._update_counter()

    def _update_counter(self, *args) -> None:
        """Refresh the character counter label."""
        self.counter.text = f"{len(self.source_text or '')} / {self.max_length}"

    def get(self) -> str:
        """Return the current text."""
        return self.text_input.text or ""

    def set(self, value: str) -> None:
        """Replace the current text."""
        self.text_input.text = value or ""
