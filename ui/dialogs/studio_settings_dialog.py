from mediapipe.tasks.cc.vision.gesture_recognizer.proto import gesture_classifier_graph_options_pb2
from mediapipe.tasks.cc.vision.gesture_recognizer.proto import gesture_classifier_graph_options_pb2
from mediapipe.tasks.cc.vision.gesture_recognizer.proto import gesture_classifier_graph_options_pb2
from mediapipe.tasks.cc.vision.gesture_recognizer.proto import gesture_classifier_graph_options_pb2
from mediapipe.tasks.cc.vision.gesture_recognizer.proto import gesture_classifier_graph_options_pb2
from mediapipe.tasks.cc.vision.gesture_recognizer.proto import gesture_classifier_graph_options_pb2
from mediapipe.tasks.cc.vision.gesture_recognizer.proto import gesture_classifier_graph_options_pb2
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QWidget,
    QLineEdit,
    QTextEdit,
    QComboBox,
    QMessageBox,
    QStackedWidget,
)
from PySide6.QtCore import Qt

from ui.theme_manager import (
    get_theme_names,
    set_theme
)


class StudioSettingsDialog(QDialog):

    def __init__(self, studio, parent=None):
        super().__init__(parent)
        self.studio = studio
        self.setWindowTitle("Studio Settings")
        self.resize(700, 450)
        layout = QVBoxLayout(self)
        title = QLabel(f"{studio['icon']} {studio['name']} Settings")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        # Main content area
        content = QHBoxLayout()
        layout.addLayout(content)

        # Left navigation
        self.nav = QListWidget()
        self.nav.addItems([
            "General",
            "Appearance",
            "Gestures",
            "Automation",
            "Advanced"
        ])
        self.nav.setFixedWidth(180)

        content.addWidget(self.nav)
        self.pages = QStackedWidget()
        content.addWidget(self.pages)
        self.general_page = QWidget()
        general_layout = QVBoxLayout(self.general_page)
        self.name_input = QLineEdit(studio["name"])

        self.desc_input = QTextEdit()
        self.desc_input.setPlainText(studio["description"])

        self.icon_input = QComboBox()
        self.icon_input.addItems([
            "💻 Coding",
            "🎨 Creative",
            "🎮 Gaming",
            "📚 Study",
            "🎬 Video",
            "🎵 Music",
            "📷 Photography",
            "🌐 Web",
            "🧠 AI",
            "⚙️ Utilities",
            "📊 Business",
            "🚀 Startup"
        ])

        for i in range(self.icon_input.count()):
            if self.icon_input.itemText(i).startswith(studio["icon"]):
                self.icon_input.setCurrentIndex(i)
                break


        general_layout.addWidget(QLabel("Studio Name"))
        general_layout.addWidget(self.name_input)

        general_layout.addWidget(QLabel("Description"))
        general_layout.addWidget(self.desc_input)

        general_layout.addWidget(QLabel("Icon"))
        general_layout.addWidget(self.icon_input)
        general_layout.addStretch()

        self.pages.addWidget(self.general_page)

        self.appearance_page = QWidget()
        appearance_layout = QVBoxLayout(self.appearance_page)

        appearance_layout.addWidget(QLabel("🎨 Appearance Settings"))
        appearance_layout.addWidget(QLabel("Theme"))

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(get_theme_names())

        appearance_layout.addWidget(self.theme_combo)
        appearance_layout.addStretch()

        self.pages.addWidget(self.appearance_page)

        self.gesture_page = QWidget()
        gesture_layout = QVBoxLayout(self.gesture_page)
        gesture_layout.addWidget(QLabel("✋ Gesture Settings"))
        gesture_layout.addStretch()
        self.pages.addWidget(self.gesture_page)

        self.automation_page = QWidget()
        automation_layout = QVBoxLayout(self.automation_page)
        automation_layout.addWidget(QLabel("⚙ Automation Settings"))
        automation_layout.addStretch()
        self.pages.addWidget(self.automation_page)

        self.advanced_page = QWidget()
        advanced_layout = QVBoxLayout(self.advanced_page)
        advanced_layout.addWidget(QLabel("🔧 Advanced Settings"))
        advanced_layout.addStretch()
        self.pages.addWidget(self.advanced_page)
        
        # Right page
        
        buttons = QHBoxLayout()

        self.delete_btn = QPushButton("🗑 Delete Studio")
        self.delete_btn.setStyleSheet("""
        QPushButton {
            background-color: #C62828;
            color: white;
            border-radius: 8px;
            padding: 8px;
        }

        QPushButton:hover {
            background-color: #E53935;
        }
        """)

        buttons.addWidget(self.delete_btn)

        buttons.addStretch()

        self.cancel_btn = QPushButton("Cancel")
        self.save_btn = QPushButton("Save Changes")

        buttons.addWidget(self.cancel_btn)
        buttons.addWidget(self.save_btn)
        layout.addLayout(buttons)
        self.cancel_btn.clicked.connect(self.reject)
        self.save_btn.clicked.connect(self.save_changes)
        self.delete_btn.clicked.connect(self.delete_studio)

        self.nav.currentRowChanged.connect(
            self.pages.setCurrentIndex
        )
        self.nav.setCurrentRow(0)

    def save_changes(self):
        self.parent().studio_manager.update_studio(
            self.studio["id"],
            self.name_input.text(),
            self.desc_input.toPlainText(),
            self.icon_input.currentText().split()[0],
            self.theme_combo.currentText()
        )

        set_theme(
            self.theme_combo.currentText()
        )
        main_window = self.window()

        if hasattr(main_window, "refresh_theme"):
            main_window.refresh_theme()
            
        self.accept()

    def delete_studio(self):
        reply = QMessageBox.question(
            self,
            "Delete Studio",
            f"Are you sure you want to delete '{self.studio['name']}'?\n\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.parent().studio_manager.delete_studio(
                self.studio["id"]
            )
            self.accept()
        
