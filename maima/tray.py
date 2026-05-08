
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QObject, pyqtSignal

class TrayIcon(QSystemTrayIcon):
    capture_requested = pyqtSignal()
    settings_requested = pyqtSignal()
    exit_requested = pyqtSignal()

    def __init__(self, parent=None):
        import os
        import sys
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        logo_path = os.path.join(base_path, "maima/assets/logo.png")
        if os.path.exists(logo_path):
            icon = QIcon(logo_path)
        else:
            from PyQt6.QtGui import QPixmap, QColor
            pixmap = QPixmap(32, 32)
            pixmap.fill(QColor(0, 123, 255))
            icon = QIcon(pixmap)
        
        super().__init__(icon, parent)
        self.setToolTip("Maima - Capture what matters")
        
        self.menu = QMenu()
        
        self.capture_action = QAction("Start Capture")
        self.capture_action.triggered.connect(self.capture_requested.emit)
        self.menu.addAction(self.capture_action)
        
        self.settings_action = QAction("Settings")
        self.settings_action.triggered.connect(self.settings_requested.emit)
        self.menu.addAction(self.settings_action)
        
        self.menu.addSeparator()
        
        self.exit_action = QAction("Exit")
        self.exit_action.triggered.connect(self.exit_requested.emit)
        self.menu.addAction(self.exit_action)
        
        self.setContextMenu(self.menu)
