# Image Toolkit 📸

A lightweight, professional utility for batch image processing. Built with Python 3.10+ and PySide6, this toolkit is designed for users who need a fast, private way to resize and scrub metadata from their images before sharing them online.

---

## ✨ Features

- **Privacy Mode**: Automatic removal of EXIF metadata to scrub GPS location, camera details, and private timestamps.
- **Batch Processing**: Drag and drop multiple files (PNG, JPG, WebP, GIF) for simultaneous processing.
- **Smart Resizing**: High-quality interpolation (LANCZOS) to scale images to specific pixel constraints.
- **Compression Control**: Adjustable quality settings to balance file size and visual clarity.
- **Flexible Output**: Save processed images individually or bundled into a single timestamped ZIP archive.
- **Adaptive UI**: A native-feeling interface that automatically snaps its height to fit the active settings.

---

## 🛠 Project Structure

The application follows a modular architecture, making it easy to extend or debug:

- `main.py`: The application controller and entry point.
- `ui_components.py`: Custom UI widgets (DropArea, Settings Groups).
- `processor.py`: The image manipulation engine powered by Pillow.
- `utils.py`: File system helpers and path management.

---

## 🚀 Getting Started

### 1. Prerequisites

Ensure you have Python 3.10 or higher installed. You can check your version by running:

```bash
python --version
```

### 2. Installation & Setup

It is highly recommended to use a virtual environment to keep your global Python installation clean.

#### macOS / Linux

```bash
# Clone the repository
git clone https://github.com/nf1973/Image-Toolkit.git
cd image-toolkit

# Create and activate environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Windows

```bash
# Clone the repository
git clone https://github.com/nf1973/Image-Toolkit.git
cd image-toolkit

# Create and activate environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the App

Once the dependencies are installed, launch the toolkit:

```bash
python main.py
```

---

## 📦 Creating a Standalone App

To package this toolkit into a single executable (a `.app` for macOS or `.exe` for Windows):

### Install PyInstaller

```bash
pip install pyinstaller
```

### Generate the Bundle

#### macOS

```bash
pyinstaller --noconsole --onedir --windowed --name "ImageToolkit" --icon=images/ImageToolkit.icns main.py
```

After building, find your application in the `dist/` folder as `ImageToolkit.app`.

---

#### Windows

```bash
pyinstaller --noconsole --onedir --windowed --name "ImageToolkit" --icon=images/ImageToolkit.ico main.py
```

After building, find your application in the `dist/` folder as `ImageToolkit.exe`.

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 🤝 Contributing

- Contributions are welcome!
- If you have a feature request or a bug report, please open an issue or submit a pull request.