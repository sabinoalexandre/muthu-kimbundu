"""Helpers for creating KivyMD Material Design buttons."""

from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivymd.uix.button import MDButton, MDButtonText

DEFAULT_BUTTON_STYLE = "text"


def create_mdbutton(
    text: str,
    on_release=None,
    style: str = DEFAULT_BUTTON_STYLE,
    size_hint_x=None,
    width=None,
    size_hint_y=None,
    height=None,
):
    """Create a KivyMD text button with the given label and action."""
    button = MDButton(style=style)
    button.add_widget(MDButtonText(text=text))
    if on_release is not None:
        button.bind(on_release=on_release)
    if size_hint_x is not None:
        button.size_hint_x = size_hint_x
    if width is not None:
        button.width = width
    if size_hint_y is not None:
        button.size_hint_y = size_hint_y
    if height is not None:
        button.height = height
    return button
