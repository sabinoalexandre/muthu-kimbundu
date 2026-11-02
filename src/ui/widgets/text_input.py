"""Multi-line text input widget with character counter."""

from kivy.metrics import dp, sp
from kivy.graphics import Color, Line, RoundedRectangle
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput as KivyTextInput
from kivymd.uix.label import MDLabel

from src.ui.widgets.theme import ACCENT_BLUE, MUTED, SURFACE


class SourceTextInput(BoxLayout):
    """Multi-line source text input area with a character counter."""

    source_text = StringProperty("")
    max_length = NumericProperty(5000)

    def __init__(self, max_length: int = 5000, **kwargs) -> None:
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = dp(4)
        self.padding = [dp(14), dp(12), dp(14), dp(8)]
        self.max_length = max_length
        with self.canvas.before:
            self._background_color = Color(*SURFACE)
            self._background = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(18)])
        with self.canvas.after:
            self._border_color = Color(0.84, 0.91, 0.97, 1)
            self._border = Line(
                rounded_rectangle=(*self.pos, *self.size, dp(18)),
                width=dp(1),
            )
        self.bind(pos=self._sync_background, size=self._sync_background)
        self.text_input = KivyTextInput(
            multiline=True,
            font_size=sp(17),
            padding=[dp(6), dp(8), dp(6), dp(6)],
            background_color=(0, 0, 0, 0),
            foreground_color=(0.12, 0.17, 0.23, 1),
            cursor_color=ACCENT_BLUE,
            hint_text_color=(0.43, 0.53, 0.63, 1),
            hint_text="Escreva uma palavra ou expressão…",
        )
        self.counter = MDLabel(
            text="0 / 5000 caracteres",
            size_hint_y=None,
            height=dp(20),
            halign="right",
            valign="middle",
            theme_text_color="Custom",
            text_color=MUTED,
            font_size=sp(11),
            font_style="Label",
            role="small",
        )
        self.add_widget(self.text_input)
        self.add_widget(self.counter)
        self.bind(source_text=self._update_counter, max_length=self._update_counter)
        self.text_input.bind(text=self._on_text)
        self.text_input.bind(focus=self._on_focus)

    def _sync_background(self, *_args) -> None:
        self._background.pos = self.pos
        self._background.size = self.size
        self._border.rounded_rectangle = (*self.pos, *self.size, dp(18))

    def _on_focus(self, _instance, focused: bool) -> None:
        """Highlight the writing surface when it is ready for input."""
        self._border_color.rgba = ACCENT_BLUE if focused else (0.84, 0.91, 0.97, 1)
        self._border.width = dp(1.5) if focused else dp(1)

    def _on_text(self, instance, value) -> None:
        """Keep the bound property and the character counter in sync."""
        self.source_text = value
        self._update_counter()

    def _update_counter(self, *args) -> None:
        """Refresh the character counter label."""
        self.counter.text = f"{len(self.source_text or '')} / {self.max_length} caracteres"

    def get(self) -> str:
        """Return the current text."""
        return self.text_input.text or ""

    def set(self, value: str) -> None:
        """Replace the current text."""
        self.text_input.text = value or ""
