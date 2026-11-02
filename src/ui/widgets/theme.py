"""Small shared drawing helpers for the MUTHU mobile interface."""

from kivy.graphics import Color, Rectangle

# Material Light Blue: an icy canvas, white surfaces, and a deep action blue.
PAGE_BACKGROUND = (0.96, 0.98, 1.0, 1)  # #F5FAFF
SURFACE = (1, 1, 1, 1)
ACCENT_BLUE = (0.008, 0.467, 0.741, 1)  # #0277BD, Light Blue 800
PALE_BLUE = (0.882, 0.961, 0.996, 1)  # #E1F5FE, Light Blue 50
MUTED = (0.32, 0.40, 0.48, 1)  # cool slate for secondary text


def apply_page_background(widget, color=PAGE_BACKGROUND):
    """Paint a full-page background that follows the widget's bounds."""
    with widget.canvas.before:
        Color(*color)
        background = Rectangle(pos=widget.pos, size=widget.size)
    widget.bind(pos=lambda instance, value: setattr(background, "pos", value))
    widget.bind(size=lambda instance, value: setattr(background, "size", value))
