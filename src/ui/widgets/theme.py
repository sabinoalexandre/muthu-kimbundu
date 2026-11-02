"""Small shared drawing helpers for the MUTHU mobile interface."""

from kivy.graphics import Color, Rectangle

PAGE_BACKGROUND = (0.95, 0.97, 0.96, 1)
SURFACE = (1, 1, 1, 1)
TEAL = (0.03, 0.36, 0.33, 1)
MUTED = (0.38, 0.47, 0.46, 1)


def apply_page_background(widget, color=PAGE_BACKGROUND):
    """Paint a full-page background that follows the widget's bounds."""
    with widget.canvas.before:
        Color(*color)
        background = Rectangle(pos=widget.pos, size=widget.size)
    widget.bind(pos=lambda instance, value: setattr(background, "pos", value))
    widget.bind(size=lambda instance, value: setattr(background, "size", value))
