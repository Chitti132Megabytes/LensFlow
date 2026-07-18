import math
import datetime
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, 
    QFrame, QComboBox, QSlider, QScrollArea, QLineEdit, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QPainter, QColor, QPen, QPainterPath
from ui.theme import (
    HoverCard, ModernButton, BG_PRIMARY, BG_CARD, BORDER_COLOR, 
    ACCENT, SUCCESS, TEXT_PRIMARY, TEXT_MUTED, get_font, WARM_AMBER, WARM_ROSE
)
from ui.right_panel import RightPanel
from backend.studios.studio_manager import StudioManager
from backend.automation.flow_manager import FlowManager

# --- APP PILL ---

class AppPill(QLabel):
    """
    A small badged app icon/label inside Studio cards.
    """
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.studio_manager = StudioManager()
        self.flow_manager = FlowManager()
        self.setFont(get_font(8, bold=True))
        self.setStyleSheet(f"""
            QLabel {{
                background-color: #1F2937;
                color: #D1D5DB;
                border: 1px solid {BORDER_COLOR};
                border-radius: 6px;
                padding: 3px 8px;
            }}
        """)


# --- STUDIO CARD ---

class StudioCard(QFrame):
    """
    A premium floating Studio card featuring micro-interactions,
    active apps, and linear gradient trigger actions.
    """
    clicked = Signal(str)  # Emits Studio name when the primary action is clicked
    
    def __init__(self, name, icon, desc, apps, last_used="", is_create_card=False, parent=None):
        super().__init__(parent)
        self.name = name
        self.icon = icon
        self.is_create_card = is_create_card
        
        # Subtle Drop Shadow
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(16)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.shadow.setOffset(0, 4)
        self.setGraphicsEffect(self.shadow)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(18, 18, 18, 18)
        self.layout.setSpacing(12)
        
        if is_create_card:
            self.set_create_style()
            self.layout.setAlignment(Qt.AlignCenter)
            
            icon_lbl = QLabel(icon)
            icon_lbl.setFont(get_font(24))
            icon_lbl.setAlignment(Qt.AlignCenter)
            
            name_lbl = QLabel(name)
            name_lbl.setFont(get_font(12, bold=True))
            name_lbl.setStyleSheet(f"color: {ACCENT};")
            name_lbl.setAlignment(Qt.AlignCenter)
            
            desc_lbl = QLabel(desc)
            desc_lbl.setFont(get_font(9))
            desc_lbl.setStyleSheet(f"color: {TEXT_MUTED};")
            desc_lbl.setAlignment(Qt.AlignCenter)
            desc_lbl.setWordWrap(True)
            
            self.layout.addStretch()
            self.layout.addWidget(icon_lbl)
            self.layout.addWidget(name_lbl)
            self.layout.addWidget(desc_lbl)
            self.layout.addStretch()
            self.setCursor(Qt.PointingHandCursor)
        else:
            self.set_normal_style()
            
            # Header Row
            header = QHBoxLayout()
            header.setSpacing(8)
            icon_lbl = QLabel(icon)
            icon_lbl.setFont(get_font(14))
            name_lbl = QLabel(name)
            name_lbl.setFont(get_font(11, bold=True))
            name_lbl.setStyleSheet("color: white;")
            header.addWidget(icon_lbl)
            header.addWidget(name_lbl)
            header.addStretch()
            self.layout.addLayout(header)
            
            # Subtitle Description
            desc_lbl = QLabel(desc)
            desc_lbl.setFont(get_font(9))
            desc_lbl.setStyleSheet(f"color: {TEXT_MUTED};")
            desc_lbl.setWordWrap(True)
            self.layout.addWidget(desc_lbl)
            
            # Integrated Apps Row
            apps_lay = QHBoxLayout()
            apps_lay.setSpacing(6)
            apps_lay.setAlignment(Qt.AlignLeft)
            for app in apps:
                pill = AppPill(app)
                apps_lay.addWidget(pill)
            self.layout.addLayout(apps_lay)
            
            # Footer Row
            footer = QHBoxLayout()
            last_lbl = QLabel(last_used)
            last_lbl.setFont(get_font(8))
            last_lbl.setStyleSheet(f"color: {TEXT_MUTED};")
            
            # Customize action button copy based on studio
            action_text = "Enter Studio →"
            if name == "Gaming":
                action_text = "Play →"
            elif name == "Study":
                action_text = "Focus →"
            elif name == "Presentation":
                action_text = "Present →"
                
            self.btn_action = ModernButton(action_text, gradient=True)
            self.btn_action.setFixedHeight(30)
            self.btn_action.clicked.connect(self.on_btn_clicked)
            
            footer.addWidget(last_lbl)
            footer.addStretch()
            footer.addWidget(self.btn_action)
            self.layout.addLayout(footer)
            
    def on_btn_clicked(self):
        self.clicked.emit(self.name)
        
    def set_normal_style(self):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {BG_CARD};
                border-radius: 14px;
                border: 1px solid {BORDER_COLOR};
            }}
        """)
        
    def set_hover_style(self):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #2D2D30;
                border-radius: 14px;
                border: 1px solid {ACCENT};
            }}
        """)
        
    def set_create_style(self):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: transparent;
                border-radius: 14px;
                border: 2px dashed {BORDER_COLOR};
            }}
        """)
        
    def set_create_hover_style(self):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #1F1F23;
                border-radius: 14px;
                border: 2px dashed {ACCENT};
            }}
        """)
        
    def enterEvent(self, event):
        if self.is_create_card:
            self.set_create_hover_style()
            self.shadow.setColor(QColor(124, 58, 237, 40))
        else:
            self.set_hover_style()
            self.shadow.setColor(QColor(124, 58, 237, 50))
            
        self.shadow.setBlurRadius(24)
        self.shadow.setOffset(0, 6)
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        if self.is_create_card:
            self.set_create_style()
        else:
            self.set_normal_style()
            
        self.shadow.setBlurRadius(16)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.shadow.setOffset(0, 4)
        super().leaveEvent(event)
        
    def mousePressEvent(self, event):
        if self.is_create_card:
            self.clicked.emit("CreateStudio")
        super().mousePressEvent(event)


# --- TOP BAR ---

class TopBar(QWidget):
    """
    Sleek minimal top bar containing logo, search placeholder, and user profile avatar.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(60)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(30, 0, 30, 0)
        layout.setSpacing(20)
        
        # Logo
        logo = QLabel("LensFlow")
        logo.setFont(get_font(12, bold=True))
        logo.setStyleSheet("color: white;")
        layout.addWidget(logo)
        
        # Search Bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search anything... (Ctrl + K)")
        self.search_bar.setFixedWidth(260)
        self.search_bar.setStyleSheet(f"""
            QLineEdit {{
                background-color: #1F2937;
                border: 1px solid {BORDER_COLOR};
                border-radius: 8px;
                padding: 6px 12px 6px 30px;
                color: {TEXT_PRIMARY};
            }}
        """)
        
        # Overlay search icon emoji in search bar
        self.search_icon = QLabel("🔍", self.search_bar)
        self.search_icon.setFont(get_font(9))
        self.search_icon.setStyleSheet("color: #9CA3AF; background: transparent;")
        self.search_icon.move(10, 8)
        
        layout.addWidget(self.search_bar)
        layout.addStretch()
        
        # Notification Bell
        self.bell = QLabel("🔔")
        self.bell.setFont(get_font(12))
        self.bell.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self.bell)
        
        # User Avatar
        self.avatar = QFrame()
        self.avatar.setFixedSize(32, 32)
        self.avatar.setStyleSheet("""
            background-color: #7C3AED;
            border-radius: 16px;
        """)
        avatar_lay = QHBoxLayout(self.avatar)
        avatar_lay.setContentsMargins(0, 0, 0, 0)
        
        avatar_txt = QLabel("P")
        avatar_txt.setFont(get_font(9, bold=True))
        avatar_txt.setAlignment(Qt.AlignCenter)
        avatar_txt.setStyleSheet("color: white; border: none;")
        avatar_lay.addWidget(avatar_txt)
        
        layout.addWidget(self.avatar)


# --- PAGES ---

class DashboardHome(QWidget):
    workspace_changed = Signal(str)  # Emits Studio name
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.studio_manager = StudioManager()
        self.flow_manager = FlowManager()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Embed minimal Top Bar
        self.top_bar = TopBar()
        self.layout.addWidget(self.top_bar)
        
        # Workspace content area
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(30, 20, 30, 30)
        content_layout.setSpacing(24)
        
        # Greeting Header
        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)
        
        # Dynamically set greeting based on local time
        now = datetime.datetime.now()
        if now.hour < 12:
            greet_text = "Good Morning, Praveena 👋"
        elif now.hour < 17:
            greet_text = "Good Afternoon, Praveena 👋"
        else:
            greet_text = "Good Evening, Praveena 👋"
            
        self.greeting = QLabel(greet_text)
        self.greeting.setFont(get_font(20, bold=True))
        self.greeting.setStyleSheet("color: white;")
        
        self.subgreeting = QLabel("Choose a Studio and continue where you left off.")
        self.subgreeting.setFont(get_font(12))
        self.subgreeting.setStyleSheet(f"color: {TEXT_MUTED};")
        
        header_layout.addWidget(self.greeting)
        header_layout.addWidget(self.subgreeting)
        content_layout.addLayout(header_layout)
        
        # Responsive 3-Column Grid of Studio Cards
        self.grid = QGridLayout()
        self.grid.setSpacing(16)
        
        self.studios = [
            ("Coding", "💻", "Everything is ready. Pick up where you left off.", ["VS Code", "Chrome", "GitHub"], "Last used • 18 mins ago"),
            ("Creative", "🎨", "Your creative tools are waiting.", ["Figma", "Photoshop", "Pinterest"], "Last used • Yesterday"),
            ("Gaming", "🎮", "Ready when you are.", ["Discord", "Steam", "Spotify"], "Last used • 2 hours ago"),
            ("Study", "📚", "Your references and notes are open.", ["Notion", "Acrobat", "Spotify"], "Last used • 3 days ago"),
            ("Presentation", "📹", "Slide deck ready.", ["PowerPoint", "Acrobat", "Spotify"], "Last used • Last week")
        ]
        
        self.cards = []
        for idx, (name, icon, desc, apps, last) in enumerate(self.studios):
            card = StudioCard(name, icon, desc, apps, last_used=last)
            card.clicked.connect(self.on_studio_click)
            self.cards.append(card)
            
            row = idx // 3
            col = idx % 3
            self.grid.addWidget(card, row, col)
            
        # Add primary Create Studio card at the end
        self.btn_create_studio = StudioCard(
            name="Create Studio",
            icon="➕",
            desc="Design a new workspace custom tailored to your routines.",
            apps=[],
            is_create_card=True
        )
        self.btn_create_studio.clicked.connect(self.on_studio_click)
        self.grid.addWidget(self.btn_create_studio, 1, 2) # row 1, column 2
        
        content_layout.addLayout(self.grid, 1)
        self.layout.addWidget(content_widget, 1)

    def on_studio_click(self, name):

        # Keep the existing signal
        self.workspace_changed.emit(name)

        # Ignore the create button for now
        if name == "Create Studio":
            print("Create Studio clicked")
            return

        # Look up the studio
        studio = self.studio_manager.get_studio(name.lower())

        if not studio:
            print(f"Studio not found: {name}")
            return

        print(f"Opening {studio['name']} Studio")

        # Execute the linked flow
        self.flow_manager.execute_flow(studio["flow"])


class FlowsPage(QWidget):
    """
    The hero feature - visual flow pipeline configurations
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 24)
        layout.setSpacing(20)
        
        # Left side: existing flows list
        left_panel = QVBoxLayout()
        left_panel.setSpacing(12)
        
        title = QLabel("⚡ Flows")
        title.setFont(get_font(18, bold=True))
        left_panel.addWidget(title)
        
        flows_scroll = QScrollArea()
        flows_scroll.setWidgetResizable(True)
        flows_scroll.setStyleSheet("background: transparent; border: none;")
        
        flows_list_widget = QWidget()
        flows_list_layout = QVBoxLayout(flows_list_widget)
        flows_list_layout.setSpacing(10)
        flows_list_layout.setContentsMargins(0, 0, 0, 0)
        
        flow_data = [
            ("Coding Flow", "Launched by Thumbs Up", True),
            ("Presentation Setup", "Launched by Peace Sign", False),
            ("Gaming Mode", "Launched by OK Gesture", False),
            ("Media Controller", "Launched by Index Finger", False),
        ]
        
        for name, desc, active in flow_data:
            card = HoverCard()
            card_lay = QVBoxLayout(card)
            card_lay.setContentsMargins(15, 12, 15, 12)
            card_lay.setSpacing(4)
            
            c_header = QHBoxLayout()
            c_title = QLabel(name)
            c_title.setFont(get_font(10, bold=True))
            c_header.addWidget(c_title)
            
            if active:
                badge = QLabel("Active")
                badge.setFont(get_font(8, bold=True))
                badge.setStyleSheet(f"background-color: {SUCCESS}; color: white; border-radius: 4px; padding: 2px 6px;")
                c_header.addWidget(badge, 0, Qt.AlignRight)
                
            c_desc = QLabel(desc)
            c_desc.setFont(get_font(9))
            c_desc.setStyleSheet(f"color: {TEXT_MUTED};")
            
            card_lay.addLayout(c_header)
            card_lay.addWidget(c_desc)
            flows_list_layout.addWidget(card)
            
        flows_list_layout.addStretch()
        flows_scroll.setWidget(flows_list_widget)
        left_panel.addWidget(flows_scroll, 1)
        
        # Right side: flow designer
        right_panel = QVBoxLayout()
        right_panel.setSpacing(12)
        
        editor_title = QLabel("FLOW DESIGNER")
        editor_title.setFont(get_font(8, bold=True))
        editor_title.setStyleSheet(f"color: {TEXT_MUTED};")
        right_panel.addWidget(editor_title)
        
        editor_card = QFrame()
        editor_card.setStyleSheet(f"""
            QFrame {{
                background-color: {BG_CARD};
                border-radius: 12px;
                border: 1px solid {BORDER_COLOR};
            }}
        """)
        ed_layout = QVBoxLayout(editor_card)
        ed_layout.setContentsMargins(20, 20, 20, 20)
        ed_layout.setSpacing(16)
        
        fd_header = QHBoxLayout()
        fd_title = QLabel("Coding Flow")
        fd_title.setFont(get_font(14, bold=True))
        fd_header.addWidget(fd_title)
        
        btn_run = ModernButton("Run Test", primary=True)
        btn_run.setFixedHeight(30)
        fd_header.addWidget(btn_run, 0, Qt.AlignRight)
        ed_layout.addLayout(fd_header)
        
        steps_lay = QVBoxLayout()
        steps_lay.setSpacing(12)
        
        steps = [
            ("1. Launch Application", "Target: Chrome (C:\\Program Files...)", "🚀"),
            ("2. Delay Wait Timer", "Duration: 2.0 seconds", "⏳"),
            ("3. Navigate URL Webpage", "URL: https://github.com", "🌐")
        ]
        
        for s_title, s_desc, s_icon in steps:
            s_widget = QFrame()
            s_widget.setStyleSheet(f"background-color: #1F2937; border-radius: 8px; border: 1px solid {BORDER_COLOR};")
            s_w_lay = QHBoxLayout(s_widget)
            s_w_lay.setContentsMargins(12, 10, 12, 10)
            
            icon = QLabel(s_icon)
            icon.setFont(get_font(12))
            
            lbl_lay = QVBoxLayout()
            lbl_lay.setSpacing(2)
            st_lbl = QLabel(s_title)
            st_lbl.setFont(get_font(9, bold=True))
            st_lbl.setStyleSheet("color: white;")
            sd_lbl = QLabel(s_desc)
            sd_lbl.setFont(get_font(8))
            sd_lbl.setStyleSheet(f"color: {TEXT_MUTED};")
            lbl_lay.addWidget(st_lbl)
            lbl_lay.addWidget(sd_lbl)
            
            s_w_lay.addWidget(icon)
            s_w_lay.addLayout(lbl_lay, 1)
            
            steps_lay.addWidget(s_widget)
            
        ed_layout.addLayout(steps_lay)
        ed_layout.addStretch()
        
        btn_add_step = ModernButton("+ Add Automation Action")
        ed_layout.addWidget(btn_add_step)
        
        right_panel.addWidget(editor_card, 1)
        
        layout.addLayout(left_panel, 2)
        layout.addLayout(right_panel, 3)


class WorkspacesPage(QWidget):
    """
    Profiles configurator list.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 24)
        layout.setSpacing(16)
        
        title = QLabel("👤 Profiles Configurator")
        title.setFont(get_font(18, bold=True))
        layout.addWidget(title)
        
        grid = QGridLayout()
        grid.setSpacing(16)
        
        workspaces = [
            ("Coding Setup", "Customized for VS Code automation, Google Search, and GitHub integrations. Active when coding.", True),
            ("Gaming Setup", "Mapped to Discord, Steam launching, and recording controls. Low recognition delay active.", False),
            ("Creative Canvas", "Optimized gestures for PowerPoint, PDF navigation, and laser pointer toggles.", False),
            ("Presentation Mode", "Universal gesture profile mapping hand speed to system volume and media triggers.", False)
        ]
        
        for idx, (p_name, p_desc, active) in enumerate(workspaces):
            card = HoverCard()
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(20, 20, 20, 20)
            card_layout.setSpacing(8)
            
            h_lay = QHBoxLayout()
            lbl_name = QLabel(p_name)
            lbl_name.setFont(get_font(12, bold=True))
            h_lay.addWidget(lbl_name)
            
            if active:
                lbl_badge = QLabel("Active")
                lbl_badge.setFont(get_font(8, bold=True))
                lbl_badge.setStyleSheet(f"background-color: {SUCCESS}; color: white; border-radius: 4px; padding: 2px 6px;")
                h_lay.addWidget(lbl_badge, 0, Qt.AlignRight)
                
            lbl_desc = QLabel(p_desc)
            lbl_desc.setWordWrap(True)
            lbl_desc.setFont(get_font(9))
            lbl_desc.setStyleSheet(f"color: {TEXT_MUTED};")
            
            card_layout.addLayout(h_lay)
            card_layout.addWidget(lbl_desc)
            card_layout.addStretch()
            
            btn_activate = ModernButton("Selected Profile" if active else "Select Profile", primary=active)
            card_layout.addWidget(btn_activate)
            
            row = idx // 2
            col = idx % 2
            grid.addWidget(card, row, col)
            
        layout.addLayout(grid, 1)


class LivePage(QWidget):
    """
    Dedicated AI Telemetry Cockpit.
    Contains Camera viewfinder, AI statistics, and the pipeline timeline.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 24)
        layout.setSpacing(24)
        
        # Left Panel: Control Deck
        left_layout = QVBoxLayout()
        left_layout.setSpacing(16)
        
        title = QLabel("✋ Live AI Cockpit")
        title.setFont(get_font(18, bold=True))
        left_layout.addWidget(title)
        
        # Deploy specs card
        specs_card = QFrame()
        specs_card.setStyleSheet(f"""
            QFrame {{
                background-color: {BG_CARD};
                border: 1px solid {BORDER_COLOR};
                border-radius: 12px;
            }}
        """)
        specs_lay = QVBoxLayout(specs_card)
        specs_lay.setContentsMargins(15, 15, 15, 15)
        specs_lay.setSpacing(10)
        
        specs_lbl = QLabel("TRACKING ENGINE SPECIFICATIONS")
        specs_lbl.setFont(get_font(8, bold=True))
        specs_lbl.setStyleSheet(f"color: {TEXT_MUTED}; letter-spacing: 0.5px;")
        specs_lay.addWidget(specs_lbl)
        
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("MediaPipe Engine:"))
        lbl_v = QLabel("v2.4 (Local Pipeline)")
        lbl_v.setFont(get_font(9, bold=True))
        row1.addWidget(lbl_v, 0, Qt.AlignRight)
        specs_lay.addLayout(row1)
        
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Accelerator Platform:"))
        lbl_acc = QLabel("Local CPU (Intel OpenVINO)")
        lbl_acc.setFont(get_font(9, bold=True))
        row2.addWidget(lbl_acc, 0, Qt.AlignRight)
        specs_lay.addLayout(row2)
        
        row3 = QHBoxLayout()
        row3.addWidget(QLabel("Engine Frame Rate:"))
        lbl_fps = QLabel("30.4 FPS")
        lbl_fps.setFont(get_font(9, bold=True))
        lbl_fps.setStyleSheet(f"color: {SUCCESS};")
        row3.addWidget(lbl_fps, 0, Qt.AlignRight)
        specs_lay.addLayout(row3)
        
        left_layout.addWidget(specs_card)
        
        # Active Gestures Mappings inside the Cockpit
        gestures_card = QFrame()
        gestures_card.setStyleSheet(f"""
            QFrame {{
                background-color: {BG_CARD};
                border: 1px solid {BORDER_COLOR};
                border-radius: 12px;
            }}
        """)
        gestures_lay = QVBoxLayout(gestures_card)
        gestures_lay.setContentsMargins(15, 15, 15, 15)
        gestures_lay.setSpacing(8)
        
        g_lbl = QLabel("ACTIVE GESTURE MAPS")
        g_lbl.setFont(get_font(8, bold=True))
        g_lbl.setStyleSheet(f"color: {TEXT_MUTED}; letter-spacing: 0.5px;")
        gestures_lay.addWidget(g_lbl)
        
        gestures_lay.addWidget(QLabel("👍 Thumbs Up  →  Launch Chrome & Open GitHub"))
        gestures_lay.addWidget(QLabel("✊ Fist       →  Deactivate System Control"))
        gestures_lay.addWidget(QLabel("✋ Open Palm  →  Activate System Tracking"))
        
        left_layout.addWidget(gestures_card)
        
        self.btn_toggle = ModernButton("Start Live Camera Pipeline", primary=True)
        left_layout.addWidget(self.btn_toggle)
        left_layout.addStretch()
        
        # Right Panel: Telemetry module
        self.right_panel = RightPanel()
        # Give right panel curved borders to match the design
        self.right_panel.setStyleSheet(f"""
            QFrame {{
                background-color: {BG_CARD};
                border: 1px solid {BORDER_COLOR};
                border-radius: 14px;
            }}
        """)
        
        layout.addLayout(left_layout, 3)
        layout.addWidget(self.right_panel, 2)


class GesturesPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 24)
        layout.setSpacing(16)
        
        title = QLabel("✋ Gestures Library")
        title.setFont(get_font(18, bold=True))
        layout.addWidget(title)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(10)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        
        gestures = [
            ("✋ Open Palm", "ACTIVATE - Wake up LensFlow telemetry", True),
            ("✊ Fist", "DEACTIVATE - Put LensFlow standby", True),
            ("👍 Thumbs Up", "coding_flow - Start productivity layout", True),
            ("✌️ Peace Sign", "Launch Chrome Web browser", True),
            ("👌 OK", "Open Spotify Desktop", False),
            ("🤏 Pinch", "Mouse Left Click control", False),
            ("☝️ Index Finger", "Enter Mouse Scroll mode", False)
        ]
        
        for name, flow, active in gestures:
            card = QFrame()
            card.setStyleSheet(f"background-color: {BG_CARD}; border: 1px solid {BORDER_COLOR}; border-radius: 10px;")
            card_lay = QHBoxLayout(card)
            card_lay.setContentsMargins(15, 12, 15, 12)
            
            g_lbl = QLabel(name)
            g_lbl.setFont(get_font(11, bold=True))
            g_lbl.setStyleSheet("color: white;")
            
            flow_lbl = QLabel(f"Mapped to: {flow}" if active else "Not Mapped")
            flow_lbl.setFont(get_font(9))
            flow_lbl.setStyleSheet(f"color: {ACCENT if active else TEXT_MUTED};")
            
            btn_edit = ModernButton("Map", primary=False)
            btn_edit.setFixedWidth(80)
            btn_edit.setFixedHeight(30)
            
            card_lay.addWidget(g_lbl)
            card_lay.addWidget(flow_lbl, 1, Qt.AlignCenter)
            card_lay.addWidget(btn_edit)
            
            scroll_layout.addWidget(card)
            
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll, 1)


class SettingsPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 24, 30, 24)
        layout.setSpacing(20)
        
        title = QLabel("⚙ Settings")
        title.setFont(get_font(18, bold=True))
        layout.addWidget(title)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(20)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        
        # Camera Settings
        grp_camera = QFrame()
        grp_camera.setStyleSheet(f"background-color: {BG_CARD}; border: 1px solid {BORDER_COLOR}; border-radius: 12px;")
        gc_lay = QVBoxLayout(grp_camera)
        gc_lay.setContentsMargins(20, 20, 20, 20)
        gc_lay.setSpacing(12)
        
        gc_title = QLabel("CAMERA SETTINGS")
        gc_title.setFont(get_font(8, bold=True))
        gc_title.setStyleSheet(f"color: {TEXT_MUTED};")
        gc_lay.addWidget(gc_title)
        
        camera_row = QHBoxLayout()
        cam_lbl = QLabel("Camera Input Source:")
        cam_lbl.setFont(get_font(10))
        cam_combo = QComboBox()
        cam_combo.addItems(["Default Webcam (Index 0)", "USB Camera (Index 1)", "OBS Virtual Camera (Index 2)"])
        cam_combo.setMinimumWidth(200)
        cam_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: #18181B;
                border: 1px solid {BORDER_COLOR};
                border-radius: 6px;
                padding: 6px 12px;
                color: white;
            }}
        """)
        camera_row.addWidget(cam_lbl)
        camera_row.addWidget(cam_combo, 0, Qt.AlignRight)
        gc_lay.addLayout(camera_row)
        
        scroll_layout.addWidget(grp_camera)
        
        # Detection Parameters
        grp_detect = QFrame()
        grp_detect.setStyleSheet(f"background-color: {BG_CARD}; border: 1px solid {BORDER_COLOR}; border-radius: 12px;")
        gd_lay = QVBoxLayout(grp_detect)
        gd_lay.setContentsMargins(20, 20, 20, 20)
        gd_lay.setSpacing(15)
        
        gd_title = QLabel("DETECTION PARAMETERS")
        gd_title.setFont(get_font(8, bold=True))
        gd_title.setStyleSheet(f"color: {TEXT_MUTED};")
        gd_lay.addWidget(gd_title)
        
        hand_row = QHBoxLayout()
        hand_lbl = QLabel("Max Hands to Track:")
        hand_lbl.setFont(get_font(10))
        hand_val = QLabel("2")
        hand_val.setFont(get_font(10, bold=True))
        hand_val.setStyleSheet(f"color: {ACCENT};")
        hand_row.addWidget(hand_lbl)
        hand_row.addWidget(hand_val, 0, Qt.AlignRight)
        gd_lay.addLayout(hand_row)
        
        conf_row = QHBoxLayout()
        conf_lbl = QLabel("Minimum Confidence Threshold:")
        conf_lbl.setFont(get_font(10))
        conf_val = QLabel("0.70")
        conf_val.setFont(get_font(10, bold=True))
        conf_val.setStyleSheet(f"color: {ACCENT};")
        conf_row.addWidget(conf_lbl)
        conf_row.addWidget(conf_val, 0, Qt.AlignRight)
        gd_lay.addLayout(conf_row)
        
        slider_conf = QSlider(Qt.Horizontal)
        slider_conf.setRange(50, 95)
        slider_conf.setValue(70)
        slider_conf.setStyleSheet(f"""
            QSlider::groove:horizontal {{
                border: 1px solid {BORDER_COLOR};
                height: 6px;
                background: #18181B;
                border-radius: 3px;
            }}
            QSlider::handle:horizontal {{
                background: {ACCENT};
                width: 14px;
                margin-top: -4px;
                margin-bottom: -4px;
                border-radius: 7px;
            }}
        """)
        slider_conf.valueChanged.connect(lambda v: conf_val.setText(f"{v/100:.2f}"))
        gd_lay.addWidget(slider_conf)
        
        scroll_layout.addWidget(grp_detect)
        
        # Developer Keys
        grp_profile = QFrame()
        grp_profile.setStyleSheet(f"background-color: {BG_CARD}; border: 1px solid {BORDER_COLOR}; border-radius: 12px;")
        gp_lay = QVBoxLayout(grp_profile)
        gp_lay.setContentsMargins(20, 20, 20, 20)
        gp_lay.setSpacing(12)
        
        gp_title = QLabel("DEVELOPER CONSOLE SETTINGS")
        gp_title.setFont(get_font(8, bold=True))
        gp_title.setStyleSheet(f"color: {TEXT_MUTED};")
        gp_lay.addWidget(gp_title)
        
        dev_row = QHBoxLayout()
        dev_lbl = QLabel("Dev Server Port:")
        dev_lbl.setFont(get_font(10))
        dev_input = QLineEdit("8080")
        dev_input.setFixedWidth(100)
        dev_input.setStyleSheet(f"background: #18181B; border: 1px solid {BORDER_COLOR}; border-radius: 6px; padding: 4px; color: white;")
        dev_row.addWidget(dev_lbl)
        dev_row.addWidget(dev_input, 0, Qt.AlignRight)
        gp_lay.addLayout(dev_row)
        
        scroll_layout.addWidget(grp_profile)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll, 1)
        
        btn_save = ModernButton("Save Changes", primary=True)
        btn_save.setFixedWidth(200)
        layout.addWidget(btn_save, 0, Qt.AlignRight)
