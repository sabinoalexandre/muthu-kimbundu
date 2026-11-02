"""Small shared drawing helpers for the MUTHU mobile interface."""

from kivy.app import App
from kivy.graphics import Color, Rectangle

# Material Light Blue: an icy canvas, white surfaces, and a deep action blue.
PAGE_BACKGROUND = (0.96, 0.98, 1.0, 1)  # #F5FAFF
SURFACE = (1, 1, 1, 1)
ACCENT_BLUE = (0.008, 0.467, 0.741, 1)  # #0277BD, Light Blue 800
PALE_BLUE = (0.882, 0.961, 0.996, 1)  # #E1F5FE, Light Blue 50
MUTED = (0.32, 0.40, 0.48, 1)  # cool slate for secondary text

DARK_PAGE_BACKGROUND = (0.047, 0.067, 0.094, 1)  # #0C1118
DARK_SURFACE = (0.09, 0.12, 0.17, 1)  # #171F2B
DARK_ACCENT_BLUE = (0.055, 0.215, 0.325, 1)  # dark blue with strong white contrast
DARK_PALE_BLUE = (0.10, 0.20, 0.29, 1)
DARK_MUTED = (0.67, 0.75, 0.83, 1)


def bind_theme_color(widget, attribute, light_color, dark_color):
    """Keep a widget color in sync with the active KivyMD theme."""
    app = App.get_running_app()

    def update(*_args):
        is_dark = app is not None and app.theme_cls.theme_style == "Dark"
        if attribute == "md_bg_color" and hasattr(widget, "theme_bg_color"):
            widget.theme_bg_color = "Custom"
        setattr(widget, attribute, dark_color if is_dark else light_color)

    update()
    if app is not None:
        app.theme_cls.bind(theme_style=update)
    return update


def apply_page_background(widget, color=PAGE_BACKGROUND):
    """Paint a full-page background that follows the widget's bounds."""
    with widget.canvas.before:
        color_instruction = Color(*color)
        background = Rectangle(pos=widget.pos, size=widget.size)
    widget._muthu_page_color = color_instruction

    app = App.get_running_app()
    if app is not None:
        def update_background(*_args):
            color_instruction.rgba = (
                DARK_PAGE_BACKGROUND
                if app.theme_cls.theme_style == "Dark" and color == PAGE_BACKGROUND
                else color
            )

        update_background()
        app.theme_cls.bind(theme_style=update_background)
    widget.bind(pos=lambda instance, value: setattr(background, "pos", value))
    widget.bind(size=lambda instance, value: setattr(background, "size", value))
