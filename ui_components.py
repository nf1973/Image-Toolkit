from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QLineEdit, QSlider, QWidget
)
from PySide6.QtCore import Qt

class DropArea(QFrame):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setAcceptDrops(True)
        self.setObjectName("dropArea")
        self.setMinimumHeight(160)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(8)
 
        self.text_label = QLabel("Drag & Drop Images")
        self.text_label.setStyleSheet("font-weight: 600; color: #2D3748; font-size: 15px;")
        
        self.or_label = QLabel("or")
        self.or_label.setStyleSheet("color: #718096; font-size: 12px;")

        self.select_btn = QPushButton("Select Images")
        self.select_btn.setFixedWidth(110)
        self.select_btn.setObjectName("innerSelectBtn")
        self.select_btn.setCursor(Qt.PointingHandCursor)
        self.select_btn.clicked.connect(self.parent.select_files)

        layout.addWidget(self.text_label, 0, Qt.AlignCenter)
        layout.addWidget(self.or_label, 0, Qt.AlignCenter)
        layout.addWidget(self.select_btn, 0, Qt.AlignCenter)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("QFrame#dropArea { border-color: #007aff; background-color: #f0f7ff; }")

    def dragLeaveEvent(self, event):
        self.setStyleSheet("")

    def dropEvent(self, event):
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        self.parent.set_files(files)
        self.setStyleSheet("")
        event.acceptProposedAction()

class ResizeSettingsGroup(QWidget):
    """Encapsulates the sliders and presets for Image settings"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 10, 0, 10)
        self.layout.setSpacing(12)

        # --- Longest Side ---
        size_header = QHBoxLayout()
        size_header.addWidget(QLabel("Longest side:"))
        size_header.addStretch()
        self.size_input = QLineEdit("1024")
        self.size_input.setFixedWidth(65)
        size_header.addWidget(self.size_input)
        size_header.addWidget(QLabel("px"))
        self.layout.addLayout(size_header)

        self.size_slider = QSlider(Qt.Horizontal)
        self.size_slider.setRange(1, 3840)
        self.size_slider.setValue(1024)
        self.layout.addWidget(self.size_slider)

        size_presets = QHBoxLayout()
        for val in [512, 1024, 1920, 2048, 3840]:
            btn = QPushButton(str(val))
            btn.clicked.connect(lambda ch, v=val: self.size_slider.setValue(v))
            size_presets.addWidget(btn)
        self.layout.addLayout(size_presets)

        # --- Quality ---
        qual_header = QHBoxLayout()
        qual_header.addWidget(QLabel("Quality:"))
        qual_header.addStretch()
        self.qual_input = QLineEdit("85")
        self.qual_input.setFixedWidth(45)
        qual_header.addWidget(self.qual_input)
        qual_header.addWidget(QLabel("%"))
        self.layout.addLayout(qual_header)

        self.qual_slider = QSlider(Qt.Horizontal)
        self.qual_slider.setRange(1, 100)
        self.qual_slider.setValue(85)
        self.layout.addWidget(self.qual_slider)

        qual_presets = QHBoxLayout()
        for val in [60, 75, 85, 95, 100]:
            btn = QPushButton(f"{val}%")
            btn.clicked.connect(lambda ch, v=val: self.qual_slider.setValue(v))
            qual_presets.addWidget(btn)
        self.layout.addLayout(qual_presets)

        # Internal Sync
        self.size_slider.valueChanged.connect(lambda v: self.size_input.setText(str(v)))
        self.qual_slider.valueChanged.connect(lambda v: self.qual_input.setText(str(v)))
        self.size_input.textChanged.connect(self.sync_sliders)
        self.qual_input.textChanged.connect(self.sync_sliders)

    def sync_sliders(self):
        try:
            if self.sender() == self.size_input:
                self.size_slider.setValue(int(self.size_input.text()))
            else:
                self.qual_slider.setValue(int(self.qual_input.text()))
        except: pass