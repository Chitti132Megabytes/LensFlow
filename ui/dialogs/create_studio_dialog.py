from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit
)
from PySide6.QtWidgets import QComboBox
from PySide6.QtCore import Qt


class CreateStudioDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Create Studio")
        self.resize(450, 350)

        layout = QVBoxLayout(self)

        title = QLabel("✨ Create Studio")
        title.setAlignment(Qt.AlignCenter)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Studio Name")

        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText("Description")

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

        self.save_btn = QPushButton("Create Studio")
        self.save_btn.clicked.connect(self.create_studio)

        layout.addWidget(title)
        layout.addWidget(self.name_input)
        layout.addWidget(self.desc_input)
        layout.addWidget(self.icon_input)
        layout.addWidget(self.save_btn)

    def create_studio(self):
        self.name = self.name_input.text().strip()
        self.description = self.desc_input.toPlainText().strip()
        self.icon = self.icon_input.currentText().split()[0]
        if not self.name:
            return

        self.accept()