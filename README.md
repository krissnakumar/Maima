# Maima — Capture what matters.

Maima is a premium Windows-inspired screenshot utility that streamlines your research and documentation workflow. With Maima, you can capture any part of your screen and have it instantly inserted into a Microsoft Word document, complete with timestamps and elegant formatting.

## Features

- **Floating Widget**: A minimalist, draggable button that stays on top of all windows.
- **Precision Capture**: Full-screen overlay with crosshair cursor and live selection glow.
- **Word Integration**: Automatically appends screenshots to a `.docx` file.
- **Global Shortcut**: Use `Ctrl + Shift + S` to trigger capture from anywhere.
- **System Tray**: Quick access to settings and capture via the system tray.
- **Modern UI**: Dark mode, glassmorphism, and smooth animations.

## Tech Stack

- **Python 3.12+**
- **PyQt6**: For the premium UI and overlay logic.
- **python-docx**: For seamless Word document manipulation.
- **MSS**: For ultra-fast screen captures.
- **Pillow**: For image processing and optimization.
- **pynput**: For global hotkey listening without root privileges.

## How to Run

1. Ensure you have Python installed.
2. Run the provided script:
   ```bash
   ./run.sh
   ```

## Usage

- **Click the Maima Floating Icon**: Activates the screen capture overlay.
- **Drag to Select**: Highlight the area you want to capture.
- **Release**: The screenshot is saved and added to `Maima_Captures.docx` in the project root.
- **Right-click Tray Icon**: Access settings to change the target document or toggle timestamps.
- **Shortcut**: Press `Ctrl + Shift + S` at any time.

---

*“Every interaction should feel polished and intentional.”*
