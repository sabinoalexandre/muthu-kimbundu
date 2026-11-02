"""Small shared drawing helpers for the MUTHU mobile interface."""

from kivy.graphics import Color, Rectangle

PAGE_BACKGROUND = (0.95, 0.98, 1.0, 1)
SURFACE = (1, 1, 1, 1)
ACCENT_BLUE = (0.10, 0.42, 0.70, 1)
PALE_BLUE = (0.88, 0.94, 1.0, 1)
MUTED = (0.36, 0.45, 0.55, 1)


def apply_page_background(widget, color=PAGE_BACKGROUND):
    """Paint a full-page background that follows the widget's bounds."""
    with widget.canvas.before:
        Color(*color)
        background = Rectangle(pos=widget.pos, size=widget.size)
    widget.bind(pos=lambda instance, value: setattr(background, "pos", value))
    widget.bind(size=lambda instance, value: setattr(background, "size", value))
