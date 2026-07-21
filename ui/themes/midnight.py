class MidnightTheme:
    NAME = "Midnight"

    # Background layers — ordered from deepest to most elevated
    BG_PRIMARY = "#0F1117"       # Deepest: main window background
    BG_SIDEBAR = "#0D0F14"      # Sidebar: slightly darker than primary
    BG_SURFACE = "#1A1D27"      # Elevated surface (nested cards, sections)
    BG_CARD = "#1E2130"         # Card containers
    BG_CARD_HOVER = "#262A3A"   # Card hover state
    BG_INPUT = "#141720"        # Input fields, text areas

    # Accent system
    ACCENT = "#7C3AED"
    ACCENT_HOVER = "#9333EA"
    ACCENT_SUBTLE = "rgba(124, 58, 237, 0.12)"  # For soft accent backgrounds

    # Semantic colors
    SUCCESS = "#22C55E"
    DANGER = "#EF4444"
    WARNING = "#F59E0B"

    # Text hierarchy
    TEXT_HEADING = "#FFFFFF"     # Pure white for headings
    TEXT_PRIMARY = "#E2E8F0"    # Primary body text
    TEXT_MUTED = "#64748B"      # Secondary / caption text

    # Borders
    BORDER_COLOR = "#2A2E3D"    # Subtle border
    BORDER_HOVER = "#3D4255"    # Hover state border

    # Gradients
    GRADIENT_START = "#7C3AED"
    GRADIENT_END = "#3B82F6"