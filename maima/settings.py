
import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QCheckBox, QFileDialog,
                             QScrollArea, QFrame, QSlider, QComboBox, QSpinBox, 
                             QColorDialog, QApplication)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QColor, QIcon

class SettingsWindow(QWidget):
    settings_changed = pyqtSignal(dict)
    exit_requested = pyqtSignal()

    def __init__(self, current_settings):
        super().__init__()
        self.setWindowTitle("Maima Settings")
        self.setFixedWidth(400)
        self.setMinimumHeight(550)
        
        # Frameless but Opaque
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        
        # Set Window Icon
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        icon_path = os.path.join(base_path, "maima/assets/logo.png")
        self.setWindowIcon(QIcon(icon_path))
        self.setStyleSheet("""
            #MainContainer {
                background-color: #ffffff;
                border: 1px solid #f0f0f0;
                border-radius: 12px;
            }
            QWidget {
                color: #333;
                font-family: 'Inter', sans-serif;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                width: 0px;
            }
            QLabel#Title {
                font-size: 15px;
                font-weight: 700;
                color: #000;
            }
            QLabel#SectionTitle {
                font-size: 9px;
                font-weight: 800;
                color: #ccc;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-top: 8px;
            }
            /* Compact Inputs */
            QLineEdit, QComboBox {
                background-color: #fcfcfc;
                border: 1px solid #f0f0f0;
                border-radius: 6px;
                padding: 4px 8px;
                color: #444;
                font-size: 12px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #007bff;
            }
            /* Custom ComboBox */
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 5px solid #bbb;
                margin-right: 8px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #f0f0f0;
                selection-background-color: #007bff;
                outline: none;
            }
            /* Compact Checkbox */
            QCheckBox {
                spacing: 8px;
                font-size: 12px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border-radius: 4px;
                border: 1px solid #ddd;
                background-color: #fff;
            }
            QCheckBox::indicator:checked {
                background-color: #007bff;
                border: 1px solid #007bff;
            }
            /* Buttons */
            QPushButton#PrimaryButton {
                background-color: #007bff;
                color: white;
                border-radius: 6px;
                padding: 5px 12px;
                font-weight: 600;
                font-size: 11px;
                border: none;
            }
            QPushButton#PrimaryButton:hover {
                background-color: #0069d9;
            }
            QPushButton#CloseButton {
                background-color: transparent;
                color: #ccc;
                font-size: 16px;
                border: none;
            }
            QPushButton#CloseButton:hover {
                color: #333;
            }
            QPushButton#SecondaryButton {
                background-color: #f8f8f8;
                color: #888;
                border-radius: 4px;
                padding: 2px 6px;
                font-size: 10px;
                border: 1px solid #eee;
            }
        """)
        
        self.settings = current_settings
        
        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5) # Compact margin
        
        # Container
        self.container = QFrame()
        self.container.setObjectName("MainContainer")
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(15, 10, 15, 15) # Compact padding
        self.main_layout.addWidget(self.container)
        
        # Title Bar
        title_bar = QHBoxLayout()
        title_label = QLabel("Maima Settings")
        title_label.setObjectName("Title")
        title_bar.addWidget(title_label)
        title_bar.addStretch()
        
        close_btn = QPushButton("×")
        close_btn.setObjectName("CloseButton")
        close_btn.setFixedSize(24, 24)
        close_btn.clicked.connect(self.close)
        title_bar.addWidget(close_btn)
        
        self.container_layout.addLayout(title_bar)
        
        # Scroll Area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        inner_widget = QWidget()
        self.scroll_layout = QVBoxLayout(inner_widget)
        self.scroll_layout.setSpacing(8) # Tighter spacing
        self.scroll_layout.setContentsMargins(0, 5, 0, 0)
        
        # --- General Section ---
        self._add_section("General")
        self.startup_cb = self._add_checkbox("Launch on startup", "launch_on_startup")
        self.notif_cb = self._add_checkbox("Enable notifications", "notifications")
        
        # --- Widget Section ---
        self._add_section("Appearance")
        self.size_combo = self._add_combo("Widget Size", ["Small", "Medium", "Large"], "widget_size")
        
        # --- Capture Section ---
        self._add_section("Capture")
        self.format_combo = self._add_combo("Format", ["PNG", "JPEG"], "image_format")
        
        # --- Word Section ---
        self._add_section("Word Export")
        self.doc_path_input = self._add_path_input("Target Document", "doc_path")
        self.ts_cb = self._add_checkbox("Add Timestamps", "timestamp_toggle")
        
        # --- Hotkeys Section ---
        self._add_section("Hotkeys")
        self.hotkey_input = QLineEdit(self.settings.get("shortcut", "<ctrl>+<shift>+s"))
        self.scroll_layout.addWidget(self.hotkey_input)
        
        self.scroll_layout.addStretch()
        scroll.setWidget(inner_widget)
        self.container_layout.addWidget(scroll)
        
        # Buttons
        h_btn_layout = QHBoxLayout()
        h_btn_layout.addStretch()
        self.save_btn = QPushButton("Apply")
        self.save_btn.setObjectName("PrimaryButton")
        self.save_btn.clicked.connect(self._save_all)
        h_btn_layout.addWidget(self.save_btn)
        self.container_layout.addLayout(h_btn_layout)

    def _add_section(self, title):
        lbl = QLabel(title)
        lbl.setObjectName("SectionTitle")
        self.scroll_layout.addWidget(lbl)

    def _add_checkbox(self, label, key):
        cb = QCheckBox(label)
        cb.setChecked(self.settings.get(key, True))
        self.scroll_layout.addWidget(cb)
        return cb

    def _add_slider(self, label, min_val, max_val, key):
        layout = QVBoxLayout()
        layout.addWidget(QLabel(label))
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(self.settings.get(key, 150))
        layout.addWidget(slider)
        self.scroll_layout.addLayout(layout)
        return slider

    def _add_combo(self, label, items, key):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(label))
        combo = QComboBox()
        combo.addItems(items)
        combo.setCurrentText(str(self.settings.get(key, items[0])))
        layout.addWidget(combo)
        self.scroll_layout.addLayout(layout)
        return combo

    def _add_path_input(self, label, key):
        layout = QVBoxLayout()
        layout.addWidget(QLabel(label))
        h_layout = QHBoxLayout()
        edit = QLineEdit(self.settings.get(key, ""))
        h_layout.addWidget(edit)
        btn = QPushButton("...")
        btn.setObjectName("SecondaryButton")
        btn.clicked.connect(lambda: self._browse_file(edit))
        h_layout.addWidget(btn)
        layout.addLayout(h_layout)
        self.scroll_layout.addLayout(layout)
        return edit

    def _browse_file(self, line_edit):
        path, _ = QFileDialog.getSaveFileName(self, "Select File", "", "Word Documents (*.docx)")
        if path:
            line_edit.setText(path)

    def _save_all(self):
        new_settings = {
            "launch_on_startup": self.startup_cb.isChecked(),
            "notifications": self.notif_cb.isChecked(),
            "widget_size": self.size_combo.currentText(),
            "image_format": self.format_combo.currentText(),
            "doc_path": self.doc_path_input.text(),
            "timestamp_toggle": self.ts_cb.isChecked(),
            "shortcut": self.hotkey_input.text(),
        }
        self.settings_changed.emit(new_settings)
        self.close()
