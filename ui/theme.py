from PySide6.QtWidgets import QFrame, QGraphicsDropShadowEffect, QPushButton
from PySide6.QtGui import QColor, QFont
from PySide6.QtCore import Qt

from ui.theme_manager import get_theme


# Fonts
def get_font(size=10, bold=False):
    font = QFont("Segoe UI", size)
    if bold:
        font.setBold(True)
    return font


def get_global_style():
    theme = get_theme()

    return f"""
QMainWindow {{
    background-color: {theme.BG_PRIMARY};
}}

QWidget {{
    color: {theme.TEXT_PRIMARY};
    font-family: 'Segoe UI', -apple-system, sans-serif;
}}

QScrollBar:vertical {{
    background: transparent;
    width: 6px;
}}

QScrollBar::handle:vertical {{
    background: {theme.BORDER_COLOR};
    min-height: 20px;
    border-radius: 3px;
}}

QScrollBar::handle:vertical:hover {{
    background: {theme.ACCENT};
}}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background: transparent;
    height: 6px;
}}

QScrollBar::handle:horizontal {{
    background: {theme.BORDER_COLOR};
    min-width: 20px;
    border-radius: 3px;
}}

QScrollBar::handle:horizontal:hover {{
    background: {theme.ACCENT};
}}
"""


class HoverCard(QFrame):
    """
    Premium card container with hover effects.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFrameShape(QFrame.NoFrame)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(16)
        self.shadow.setColor(QColor(0, 0, 0, 100))
        self.shadow.setOffset(0, 4)
        self.setGraphicsEffect(self.shadow)

        self.set_normal_style()

    def set_normal_style(self):

        theme = get_theme()

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {theme.BG_CARD};
                border-radius: 16px;
                border: 1px solid {theme.BORDER_COLOR};
            }}
        """)

    def set_hover_style(self):

        theme = get_theme()

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {theme.BG_CARD_HOVER};
                border-radius: 16px;
                border: 1px solid {theme.ACCENT};
            }}
        """)

    def enterEvent(self, event):

        self.set_hover_style()

        self.shadow.setBlurRadius(24)
        self.shadow.setColor(QColor(124, 58, 237, 50))
        self.shadow.setOffset(0, 6)

        super().enterEvent(event)

    def leaveEvent(self, event):

        self.set_normal_style()

        self.shadow.setBlurRadius(16)
        self.shadow.setColor(QColor(0, 0, 0, 100))
        self.shadow.setOffset(0, 4)

        super().leaveEvent(event)


class ModernButton(QPushButton):
    """
    Modern LensFlow button.
    """

    def __init__(self, text, primary=False, gradient=False, parent=None):

        super().__init__(text, parent)

        theme = get_theme()

        self.setFont(get_font(10, bold=True))
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(40)

        if gradient:

            self.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(
                        x1:0, y1:0, x2:1, y2:0,
                        stop:0 {theme.GRADIENT_START},
                        stop:1 {theme.GRADIENT_END}
                    );
                    color: {theme.TEXT_PRIMARY};
                    border-radius: 10px;
                    border: none;
                    padding: 0 16px;
                }}

                QPushButton:hover {{
                    background-color: {theme.ACCENT_HOVER};
                }}
            """)

        elif primary:

            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {theme.ACCENT};
                    color: {theme.TEXT_PRIMARY};
                    border-radius: 10px;
                    border: none;
                    padding: 0 16px;
                }}

                QPushButton:hover {{
                    background-color: {theme.ACCENT_HOVER};
                }}
            """)

        else:

            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {theme.BG_CARD};
                    color: {theme.TEXT_PRIMARY};
                    border-radius: 10px;
                    border: 1px solid {theme.BORDER_COLOR};
                    padding: 0 16px;
                }}

                QPushButton:hover {{
                    background-color: {theme.BG_CARD_HOVER};
                }}
            """)
# Backwards compatibility for existing UI imports
theme = get_theme()

BG_PRIMARY = theme.BG_PRIMARY
BG_SIDEBAR = theme.BG_SIDEBAR
BG_CARD = theme.BG_CARD
BG_CARD_HOVER = theme.BG_CARD_HOVER

ACCENT = theme.ACCENT
ACCENT_HOVER = theme.ACCENT_HOVER

SUCCESS = theme.SUCCESS

TEXT_PRIMARY = theme.TEXT_PRIMARY
TEXT_MUTED = theme.TEXT_MUTED

BORDER_COLOR = theme.BORDER_COLOR

GRADIENT_START = theme.GRADIENT_START
GRADIENT_END = theme.GRADIENT_END

GLOBAL_STYLE = get_global_style()
# Creative colors (legacy compatibility)
WARM_AMBER = "#F59E0B"
WARM_ROSE = "#EC4899"

# Gradient fallback
GRADIENT_START = get_theme().GRADIENT_START
GRADIENT_END = get_theme().GRADIENT_END