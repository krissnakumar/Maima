
import sys
import os
import random
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QApplication, QStyleOptionButton, QStyle, QMenu, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt, QPoint, pyqtSignal, QSize, QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup, pyqtProperty, QTimer
from PyQt6.QtGui import QIcon, QPainter, QColor, QPen, QAction

class WelcomePopup(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.ToolTip | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        layout = QVBoxLayout(self)
        self.label = QLabel()
        self.label.setStyleSheet("""
            background-color: rgba(30, 30, 30, 230);
            color: white;
            padding: 8px 15px;
            border-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            font-family: 'Segoe UI Variable', sans-serif;
            font-size: 12px;
            font-weight: bold;
        """)
        layout.addWidget(self.label)
        
        # Funny messages
        messages = [
            "Ready to capture the world! 📸",
            "I'm awake! Let's screenshot something. ✨",
            "M stands for Masterpiece. Ready? 🎨",
            "Don't be shy, I'm just an 'M'. 🔘",
            "Capture queen/king is in the house! 👑"
        ]
        self.label.setText(random.choice(messages))
        
        self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_anim.setDuration(500)

    def show_animated(self, pos):
        self.move(pos.x() - self.width() // 2, pos.y() - 40)
        self.setWindowOpacity(0)
        self.show()
        self.fade_anim.setStartValue(0)
        self.fade_anim.setEndValue(1)
        self.fade_anim.start()
        QTimer.singleShot(3000, self.hide_animated)

    def hide_animated(self):
        self.fade_anim.setStartValue(1)
        self.fade_anim.setEndValue(0)
        self.fade_anim.finished.connect(self.hide)
        self.fade_anim.start()

class DraggableButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent
        self.dragging = False
        self.start_pos = None
        self._rotation = 0

    @pyqtProperty(int)
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, angle):
        self._rotation = angle
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        cx, cy = self.width() / 2, self.height() / 2
        painter.translate(cx, cy)
        painter.rotate(self._rotation)
        painter.translate(-cx, -cy)
        
        icon = self.icon()
        if not icon.isNull():
            size = self.iconSize()
            pixmap = icon.pixmap(size)
            target_rect = self.rect().adjusted(
                (self.width() - size.width()) // 2,
                (self.height() - size.height()) // 2,
                -(self.width() - size.width()) // 2,
                -(self.height() - size.height()) // 2
            )
            painter.drawPixmap(target_rect, pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.start_pos = event.globalPosition().toPoint()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.dragging:
            curr_pos = event.globalPosition().toPoint()
            delta = curr_pos - self.start_pos
            self.parent_widget.move(self.parent_widget.x() + delta.x(), self.parent_widget.y() + delta.y())
            self.start_pos = curr_pos
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.dragging = False
        super().mouseReleaseEvent(event)

class FloatingWidget(QWidget):
    clicked = pyqtSignal()
    settings_requested = pyqtSignal()
    exit_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setObjectName("FloatingWidget")
        
        self.setFixedSize(50, 50)
        self.welcome_shown = False

        self.button = DraggableButton(self)
        self.button.setObjectName("FloatingButton")
        self.button.setFixedSize(40, 40)
        self.button.move(5, 5)
        self.button.setText("")
        
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        icon_path = os.path.join(base_path, "maima/assets/logo.png")
        self.button.setIcon(QIcon(icon_path))
        self.button.setIconSize(QSize(30, 30))
        self.button.clicked.connect(self.clicked.emit)
        
        self.success_label = QLabel(self)
        self.success_label.setFixedSize(50, 50)
        self.success_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.success_label.setText("✓")
        self.success_label.setStyleSheet("color: #00ff00; font-size: 24px; font-weight: bold; background: transparent;")
        self.success_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.success_label.hide()

        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - 80, screen.height() - 120)

    def enterEvent(self, event):
        if not self.welcome_shown:
            self.welcome_shown = True
            popup = WelcomePopup()
            popup.show_animated(self.mapToGlobal(QPoint(self.width() // 2, 0)))
            # Keep reference to avoid GC
            self._welcome_popup = popup
        super().enterEvent(event)

    def show_context_menu(self, pos):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #1a1a1a;
                color: white;
                border: 1px solid #333;
                border-radius: 6px;
            }
            QMenu::item:selected {
                background-color: #007bff;
            }
        """)
        
        capture_action = QAction("Start Capture", self)
        capture_action.triggered.connect(self.clicked.emit)
        menu.addAction(capture_action)
        
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.settings_requested.emit)
        menu.addAction(settings_action)
        
        menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.exit_requested.emit)
        menu.addAction(exit_action)
        
        menu.exec(self.mapToGlobal(pos))

    def show_success(self):
        self.rot_anim = QPropertyAnimation(self.button, b"rotation")
        self.rot_anim.setDuration(600)
        self.rot_anim.setStartValue(0)
        self.rot_anim.setEndValue(360)
        self.rot_anim.setEasingCurve(QEasingCurve.Type.InOutBack)
        
        self.success_label.show()
        QTimer.singleShot(1000, self.success_label.hide)
        self.rot_anim.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = FloatingWidget()
    widget.show()
    sys.exit(app.exec())
