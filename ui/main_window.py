import sys
import os

# Insert parent directory of 'ui' at the beginning of the path list to ensure
# we can run this file directly and resolve 'ui.xxx' imports cleanly.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QStackedWidget
from PySide6.QtCore import Qt
from ui.theme import GLOBAL_STYLE, BG_PRIMARY
from ui.sidebar import Sidebar
from ui.dashboard import (
    DashboardHome, FlowsPage, WorkspacesPage, LivePage, SettingsPage
)
from ui.theme import get_global_style

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LensFlow")
        self.resize(1280, 750)
        self.setMinimumSize(1100, 680)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout (horizontal splitting)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left sidebar
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Center stacked workspace pages
        self.workspace = QStackedWidget()
        self.workspace.setStyleSheet(f"background-color: {BG_PRIMARY}; border: none;")
        
        self.page_home = DashboardHome()
        self.page_flows = FlowsPage()
        self.page_profiles = WorkspacesPage()
        self.page_live = LivePage()
        self.page_settings = SettingsPage()
        
        self.workspace.addWidget(self.page_home)       # Index 0: Home (Studio Hub)
        self.workspace.addWidget(self.page_flows)      # Index 1: Flows Designer
        self.workspace.addWidget(self.page_profiles)   # Index 2: Profiles Configuration
        self.workspace.addWidget(self.page_live)       # Index 3: Live AI Cockpit
        self.workspace.addWidget(self.page_settings)   # Index 4: Settings
        
        main_layout.addWidget(self.workspace, 1)
        
        # Connect sidebar navigation buttons to stacked index switching
        self.sidebar.tab_changed.connect(self.workspace.setCurrentIndex)
        
        # Connect home workspace selection to update right panel and switch view to Live
        self.page_home.workspace_changed.connect(self.on_workspace_selected)
        
        # Global stylesheet application
        self.setStyleSheet(get_global_style())

    def on_workspace_selected(self, studio_name):
        """
        When a user enters a Studio, set telemetry states on the Live panel
        and transition them instantly to the Live cockpit.
        """
        # Set RightPanel telemetry specific to selected Studio
        self.page_live.right_panel.set_workspace(studio_name)
        
        # Trigger Sidebar navigation selection to Live (index 3)
        self.sidebar.on_btn_clicked(3)

    def refresh_theme(self):
        self.setStyleSheet(get_global_style())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())