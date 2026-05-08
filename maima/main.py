
import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer, QSize
from PyQt6.QtGui import QIcon

# Add current directory to path to ensure imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from floating_widget import FloatingWidget
from overlay import CaptureOverlay
from word_exporter import WordExporter
from hotkeys import HotkeyManager
from tray import TrayIcon
from settings import SettingsWindow
from styles import STYLES

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class MaimaApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        self.app.setStyleSheet(STYLES)

        # Set Global App Icon
        icon_path = resource_path("maima/assets/logo.png")
        self.app.setWindowIcon(QIcon(icon_path))

        self.settings = {
            "doc_path": os.path.join(os.getcwd(), "Maima_Captures.docx"),
            "save_path": os.path.join(os.getcwd(), "maima/captures"),
            "timestamp_toggle": True,
            "launch_on_startup": False,
            "notifications": True,
            "animation_speed": 300,
            "border_color": "#007bff",
            "overlay_opacity": 150,
            "image_format": "PNG",
            "capture_delay": 0,
            "page_layout": "Portrait",
            "image_scaling": 100,
            "shortcut": "<ctrl>+<shift>+s",
            "widget_size": "Medium"
        }

        self.exporter = WordExporter(self.settings["doc_path"])
        self.overlay = None
        self.floating_widget = FloatingWidget()
        self.tray = TrayIcon()
        self.settings_window = None

        # Connections
        self.floating_widget.clicked.connect(self.start_capture)
        self.floating_widget.settings_requested.connect(self.show_settings)
        self.floating_widget.exit_requested.connect(self.exit_app)
        
        self.tray.capture_requested.connect(self.start_capture)
        self.tray.settings_requested.connect(self.show_settings)
        self.tray.exit_requested.connect(self.exit_app)

        # Hotkeys
        self.hotkey_manager = HotkeyManager(self.start_capture)
        self.hotkey_manager.start()

        self.floating_widget.show()
        self.tray.show()

    def start_capture(self):
        # We need to make sure the overlay is created in the main thread
        # especially when called from hotkeys (keyboard library runs in a separate thread)
        QTimer.singleShot(0, self._show_overlay)

    def _show_overlay(self):
        if self.overlay and self.overlay.isVisible():
            return
        
        self.overlay = CaptureOverlay(self.settings)
        self.overlay.capture_finished.connect(self.process_capture)
        self.overlay.show()

    def process_capture(self, image_path):
        success = self.exporter.add_capture(image_path, self.settings)
        if success:
            print(f"Captured and saved to Word: {image_path}")
            self.floating_widget.show_success()
        else:
            print("Failed to save capture to Word")

    def show_settings(self):
        if not self.settings_window:
            self.settings_window = SettingsWindow(self.settings)
            self.settings_window.settings_changed.connect(self.update_settings)
            self.settings_window.exit_requested.connect(self.exit_app)
        self.settings_window.show()

    def update_settings(self, new_settings):
        old_shortcut = self.settings.get("shortcut")
        old_size_str = self.settings.get("widget_size", "Medium")
        self.settings.update(new_settings)
        self.exporter = WordExporter(self.settings["doc_path"])
        
        # Handle Size Change
        if old_size_str != self.settings.get("widget_size"):
            size_map = {"Small": 40, "Medium": 60, "Large": 80}
            new_size = size_map.get(self.settings.get("widget_size"), 60)
            
            self.floating_widget.setFixedSize(new_size, new_size)
            self.floating_widget.button.setFixedSize(new_size - 10, new_size - 10)
            self.floating_widget.button.setIconSize(QSize(new_size - 20, new_size - 20))
            self.floating_widget.success_label.setFixedSize(new_size, new_size)

        # Handle Hotkey Change
        if old_shortcut != self.settings.get("shortcut"):
            self.hotkey_manager.stop()
            self.hotkey_manager = HotkeyManager(self.start_capture)
            self.hotkey_manager.shortcut_str = self.settings.get("shortcut")
            self.hotkey_manager.start()
            
        print("Settings updated")

    def exit_app(self):
        self.hotkey_manager.stop()
        self.app.quit()

    def run(self):
        sys.exit(self.app.exec())

if __name__ == "__main__":
    maima = MaimaApp()
    maima.run()
