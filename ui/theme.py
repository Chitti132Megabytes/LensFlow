from PySide6.QtWidgets import QFrame, QGraphicsDropShadowEffect, QPushButton
from PySide6.QtGui import QColor, QFont
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve

# Design Colors
BG_PRIMARY = "#18181B"
BG_SIDEBAR = "#111827"
BG_CARD = "#27272A"
BG_CARD_HOVER = "#2D2D30"
ACCENT = "#7C3AED"
ACCENT_HOVER = "#9333EA"
SUCCESS = "#22C55E"
TEXT_PRIMARY = "#F8FAFC"
TEXT_MUTED = "#A1A1AA"
BORDER_COLOR = "#3F3F46"

# Warm / Creative Colors
WARM_AMBER = "#F59E0B"
WARM_ROSE = "#EC4899"
GRADIENT_START = "#7C3AED"
GRADIENT_END = "#3B82F6"


# Fonts
def get_font(size=10, bold=False):
    font = QFont("Segoe UI", size)
    if bold:
        font.setBold(True)
    return font

# Global QSS Stylesheet
GLOBAL_STYLE = f"""
QMainWindow {{
    background-color: {BG_PRIMARY};
}}

QWidget {{
    color: {TEXT_PRIMARY};
    font-family: 'Segoe UI', -apple-system, sans-serif;
}}

/* Scrollbars */
QScrollBar:vertical {{
    background: transparent;
    width: 6px;
    margin: 0px;
}}
QScrollBar::handle:vertical {{
    background: #3F3F46;
    min-height: 20px;
    border-radius: 3px;
}}
QScrollBar::handle:vertical:hover {{
    background: {ACCENT};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background: transparent;
    height: 6px;
    margin: 0px;
}}
QScrollBar::handle:horizontal {{
    background: #3F3F46;
    min-width: 20px;
    border-radius: 3px;
}}
QScrollBar::handle:horizontal:hover {{
    background: {ACCENT};
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}
"""

class HoverCard(QFrame):
    """
    A premium card container with soft borders, rounded corners,
    subtle drop shadow, and interactive hover elevation/glow effects.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.NoFrame)
        
        # Initial shadow
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(16)
        self.shadow.setColor(QColor(0, 0, 0, 100))
        self.shadow.setOffset(0, 4)
        self.setGraphicsEffect(self.shadow)
        
        self.set_normal_style()
        
    def set_normal_style(self):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {BG_CARD};
                border-radius: 16px;
                border: 1px solid {BORDER_COLOR};
            }}
        """)
        
    def set_hover_style(self):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {BG_CARD_HOVER};
                border-radius: 16px;
                border: 1px solid {ACCENT};
            }}
        """)

    def enterEvent(self, event):
        self.set_hover_style()
        self.shadow.setBlurRadius(24)
        self.shadow.setColor(QColor(124, 58, 237, 50)) # violet soft glow
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
    A customizable flat button featuring CSS hover animations and transitions.
    """
    def __init__(self, text, primary=False, gradient=False, parent=None):
        super().__init__(text, parent)
        self.setFont(get_font(10, bold=True))
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(40)
        
        if gradient:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {GRADIENT_START}, stop:1 {GRADIENT_END});
                    color: {TEXT_PRIMARY};
                    border-radius: 10px;
                    border: none;
                    padding: 0 16px;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #8B5CF6, stop:1 #F43F5E);
                }}
                QPushButton:pressed {{
                    background: #6D28D9;
                }}
            """)
        elif primary:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {ACCENT};
                    color: {TEXT_PRIMARY};
                    border-radius: 10px;
                    border: none;
                    padding: 0 16px;
                }}
                QPushButton:hover {{
                    background-color: {ACCENT_HOVER};
                }}
                QPushButton:pressed {{
                    background-color: #6D28D9;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: #27272A;
                    color: {TEXT_PRIMARY};
                    border-radius: 10px;
                    border: 1px solid {BORDER_COLOR};
                    padding: 0 16px;
                }}
                QPushButton:hover {{
                    background-color: #3F3F46;
                    border-color: {TEXT_MUTED};
                }}
                QPushButton:pressed {{
                    background-color: #18181B;
                }}
            """)
