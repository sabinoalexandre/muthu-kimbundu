"""Helpers for creating KivyMD Material Design buttons."""

from kivy.metrics import dp, sp
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText

DEFAULT_BUTTON_STYLE = "text"


def create_mdbutton(
    text: str,
    on_release=None,
    style: str = DEFAULT_BUTTON_STYLE,
    size_hint_x=None,
    width=None,
    size_hint_y=None,
    height=None,
    icon=None,
):
    """Create a compact, rounded KivyMD button with consistent label styling."""
    button = MDButton(style=style, radius=[dp(16)])
    if icon:
        button.add_widget(MDButtonIcon(icon=icon))
    # Keep button labels on the compact Material label scale so they fit the
    # 40–54 dp mobile touch targets used throughout the app.
    button.add_widget(MDButtonText(
        text=text,
        font_size=sp(14),
        role="small",
        halign="center",
        valign="middle",
        shorten=True,
    ))
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
