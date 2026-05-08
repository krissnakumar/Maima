
from pynput import keyboard
import threading

class HotkeyManager:
    def __init__(self, callback):
        self.callback = callback
        # pynput uses a listener approach
        self.listener = None
        self.shortcut_str = "<ctrl>+<shift>+s"

    def start(self):
        # We use GlobalHotKeys for cross-platform shortcut support
        self.listener = keyboard.GlobalHotKeys({
            self.shortcut_str: self.callback
        })
        self.listener.start()

    def stop(self):
        if self.listener:
            self.listener.stop()
