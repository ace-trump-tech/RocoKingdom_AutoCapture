# utils/hotkey_listener.py
import threading
from pynput import keyboard
from typing import Callable, Optional

class HotkeyListener:
    """
    Global hotkey listener using pynput.
    Supports start, stop, and exit callbacks.
    """
    def __init__(self, config: dict):
        """
        :param config: dict containing 'hotkeys' with keys 'start', 'stop', 'exit'
                       each value is a string like "f2", "ctrl+shift+s"
        """
        self.start_hotkey = self._parse_hotkey(config['hotkeys']['start'])
        self.stop_hotkey = self._parse_hotkey(config['hotkeys']['stop'])
        self.exit_hotkey = self._parse_hotkey(config['hotkeys']['exit'])
        
        self.current_keys = set()
        self.listener: Optional[keyboard.Listener] = None
        
        self._on_start: Optional[Callable] = None
        self._on_stop: Optional[Callable] = None
        self._on_exit: Optional[Callable] = None
        
        self.lock = threading.Lock()
    
    @staticmethod
    def _parse_hotkey(hotkey_str: str):
        """Convert 'ctrl+shift+s' to ['ctrl', 'shift', 's']"""
        return hotkey_str.lower().split('+')
    
    def _normalize_key(self, key) -> str:
        """Convert a pynput key to string representation."""
        try:
            # Character key
            return key.char.lower()
        except AttributeError:
            # Special key (e.g., Key.ctrl, Key.shift)
            return key.name.lower()
    
    def _on_press(self, key):
        k = self._normalize_key(key)
        with self.lock:
            self.current_keys.add(k)
            self._check_hotkeys()
    
    def _on_release(self, key):
        k = self._normalize_key(key)
        with self.lock:
            if k in self.current_keys:
                self.current_keys.remove(k)
    
    def _check_hotkeys(self):
        # Check start hotkey
        if all(k in self.current_keys for k in self.start_hotkey):
            if self._on_start:
                self._on_start()
        # Check stop hotkey
        elif all(k in self.current_keys for k in self.stop_hotkey):
            if self._on_stop:
                self._on_stop()
        # Check exit hotkey
        elif all(k in self.current_keys for k in self.exit_hotkey):
            if self._on_exit:
                self._on_exit()
    
    def register_start_callback(self, callback: Callable):
        self._on_start = callback
    
    def register_stop_callback(self, callback: Callable):
        self._on_stop = callback
    
    def register_exit_callback(self, callback: Callable):
        self._on_exit = callback
    
    def start(self):
        """Start the listener in a background thread."""
        self.listener = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)
        self.listener.start()
    
    def stop(self):
        """Stop the listener."""
        if self.listener:
            self.listener.stop()
