
import sys
from PyQt6.QtWidgets import QWidget, QApplication, QRubberBand
from PyQt6.QtCore import Qt, QRect, QPoint, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QCursor, QPen
import mss
from PIL import Image
import os
import time

class CaptureOverlay(QWidget):
    capture_finished = pyqtSignal(str)

    def __init__(self, settings=None):
        super().__init__()
        self.settings = settings or {}
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setCursor(Qt.CursorShape.CrossCursor)
        
        self.origin = QPoint()
        self.rubber_band = QRubberBand(QRubberBand.Shape.Rectangle, self)
        
        # Capture the whole screen geometry
        self.screen_geometry = QApplication.primaryScreen().geometry()
        self.setGeometry(self.screen_geometry)
        
        self.selection_rect = QRect()
        self.overlay_opacity = self.settings.get("overlay_opacity", 150)
        self.border_color = QColor(self.settings.get("border_color", "#007bff"))

    def showEvent(self, event):
        self.setFocus(Qt.FocusReason.OtherFocusReason)
        super().showEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        # Draw semi-transparent background
        painter.fillRect(self.rect(), QColor(0, 0, 0, self.overlay_opacity))
        
        if not self.selection_rect.isNull():
            # Clear the selection area
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Clear)
            painter.fillRect(self.selection_rect, Qt.GlobalColor.transparent)
            painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceOver)
            
            # Draw border
            pen = QPen(self.border_color, 2)
            painter.setPen(pen)
            painter.drawRect(self.selection_rect)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.origin = event.pos()
            self.selection_rect = QRect(self.origin, self.origin)
            self.update()

    def mouseMoveEvent(self, event):
        if not self.origin.isNull():
            self.selection_rect = QRect(self.origin, event.pos()).normalized()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.capture_region()
            self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

    def capture_region(self):
        if self.selection_rect.width() < 5 or self.selection_rect.height() < 5:
            return

        # Map local coordinates to global
        global_rect = self.selection_rect.translated(self.geometry().topLeft())
        
        with mss.mss() as sct:
            monitor = {
                "top": global_rect.top(),
                "left": global_rect.left(),
                "width": global_rect.width(),
                "height": global_rect.height(),
            }
            sct_img = sct.grab(monitor)
            
            # Save to temporary file
            os.makedirs("maima/captures", exist_ok=True)
            filename = f"maima/captures/capture_{int(time.time())}.png"
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=filename)
            
            self.capture_finished.emit(filename)

if __name__ == "__main__":
    # Test
    app = QApplication(sys.argv)
    overlay = CaptureOverlay()
    overlay.show()
    sys.exit(app.exec())
