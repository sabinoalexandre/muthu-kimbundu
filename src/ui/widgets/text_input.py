"""Multi-line text input widget with character counter."""

from kivy.metrics import dp
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
        self.max_length = max_length
        self.text_input = KivyTextInput(
            multiline=True,
            font_size="14sp",
            padding=[8, 8, 8, 8],
        )
        self.counter = MDLabel(
            text="0 / 5000",
            size_hint_y=None,
            height=dp(20),
            halign="right",
            valign="middle",
        )
        self.add_widget(self.text_input)
        self.add_widget(self.counter)
        self.bind(source_text=self._update_counter, max_length=self._update_counter)
        self.text_input.bind(text=self._on_text)

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
