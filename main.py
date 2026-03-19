import sys
import io
import zipfile
import os
from datetime import datetime
from PIL import Image, ImageOps
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QFileDialog, QLabel, QMessageBox, QCheckBox
)
from PySide6.QtCore import Qt

from utils import get_unique_filename
from processor import resize_image
from ui_components import DropArea, ResizeSettingsGroup

class ImageResizerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Toolkit")
        self.files = []
        self.init_ui()
        self.apply_styles()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(15)

        self.drop_area = DropArea(self)
        self.drop_area.setMinimumWidth(400)
        self.exif_checkbox = QCheckBox("Remove EXIF Metadata")
        self.exif_checkbox.setChecked(True)
        
        self.resize_toggle = QCheckBox("Enable Resizing && Compression")
        self.zip_checkbox = QCheckBox("Save as ZIP archive")
        
        self.resize_settings = ResizeSettingsGroup()
        self.resize_settings.hide()
        self.resize_toggle.toggled.connect(self.toggle_resize_visibility)

        self.process_btn = QPushButton("Process and Save (0 images selected)")
        self.process_btn.setObjectName("mainAction")
        self.process_btn.setCursor(Qt.PointingHandCursor)
        self.process_btn.clicked.connect(self.process_images)
        
        self.main_layout.addWidget(self.drop_area)
        self.main_layout.addWidget(self.exif_checkbox)
        self.main_layout.addWidget(self.resize_toggle)

        self.main_layout.addWidget(self.resize_settings)
        self.main_layout.addWidget(self.zip_checkbox)
        self.main_layout.addSpacing(10)

        self.main_layout.addWidget(self.process_btn)
        self.main_layout.setSizeConstraint(QVBoxLayout.SetFixedSize)

    def toggle_resize_visibility(self, checked):
        self.resize_settings.setVisible(checked)

    def set_files(self, files):
        valid = ('.png', '.jpg', '.jpeg', '.gif', '.webp')
        self.files = [f for f in files if f.lower().endswith(valid)]
        self.update_ui_state()

    def update_ui_state(self):
        count = len(self.files)
        self.zip_checkbox.setChecked(count >= 2)
        text = "Drag & Drop Images" if count == 0 else f"{count} image{'s' if count != 1 else ''} selected"
        self.drop_area.text_label.setText(text)
        self.process_btn.setText(f"Process and Save ({count} image{'s' if count != 1 else ''} selected)")
    
    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", "Images (*.png *.jpg *.jpeg *.gif *.webp)")
        if files: self.set_files(files)

    def process_images(self):
        if not self.files:
            QMessageBox.warning(self, "No Files", "Please select images first.")
            return

        do_resize = self.resize_toggle.isChecked()
        scrub = self.exif_checkbox.isChecked()
        use_zip = self.zip_checkbox.isChecked()
        output_dir = os.path.join(os.getcwd(), "output")
        os.makedirs(output_dir, exist_ok=True)

        try:
            results = []
            for path in self.files:
                with Image.open(path) as img:
                    fmt = img.format if img.format else "JPEG"
                    if scrub: img = ImageOps.exif_transpose(img)
                    if do_resize: img = resize_image(img, self.resize_settings.size_slider.value())
                    
                    save_args = {"format": fmt}
                    if do_resize and fmt in ["JPEG", "JPG"]:
                        save_args["quality"] = self.resize_settings.qual_slider.value()

                    if scrub:
                        save_args["exif"] = b""
                        if "icc_profile" in img.info: save_args["icc_profile"] = img.info["icc_profile"]
                    else:
                        if "exif" in img.info: save_args["exif"] = img.info["exif"]
                        if "icc_profile" in img.info: save_args["icc_profile"] = img.info["icc_profile"]

                    buf = io.BytesIO()
                    img.save(buf, **save_args)
                    results.append((os.path.basename(path), buf.getvalue()))

            if use_zip:
                save_path = get_unique_filename(os.path.join(output_dir, f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"))
                with zipfile.ZipFile(save_path, 'w') as z:
                    for name, data in results: z.writestr(name, data)
            else:
                for name, data in results:
                    with open(get_unique_filename(os.path.join(output_dir, name)), "wb") as f: f.write(data)

            QMessageBox.information(self, "Success", f"Processed {len(self.files)} images!")
            self.files = []; self.update_ui_state()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget { background-color: #fbfbfb; font-family: ".AppleSystemUIFont", "Helvetica Neue", Helvetica, sans-serif; color: #2D3748; }
            #dropArea { border: 2px dashed #cbd5e0; border-radius: 16px; background-color: #ffffff; }
            #innerSelectBtn { background-color: white; border: 1px solid #cbd5e0; border-radius: 8px; padding: 6px; font-weight: 600; font-size: 11px; }
            QLineEdit { border: 1px solid #cbd5e0; border-radius: 6px; padding: 4px; background: white; font-weight: bold; }
            QPushButton { background-color: #edf2f7; border: 1px solid #cbd5e0; border-radius: 6px; padding: 5px; font-size: 10px; }
            #mainAction { background-color: #007aff; color: white; font-weight: bold; font-size: 14px; padding: 12px; border-radius: 10px; border: none; }
            #mainAction:hover { background-color: #0063d1; }
            QSlider::groove:horizontal { height: 4px; background: #e2e8f0; }
            QSlider::handle:horizontal { background: #007aff; width: 14px; height: 14px; margin: -5px 0; border-radius: 7px; }
            QCheckBox { font-size: 13px; font-weight: 500; }
            #statusLabel { color: #718096; font-size: 12px; }
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageResizerApp()
    window.show()
    sys.exit(app.exec())