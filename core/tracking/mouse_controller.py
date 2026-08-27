# core/tracking/mouse_controller.py
import pyautogui
import time
import numpy as np
from pynput.mouse import Controller as MouseControllerLib

class MouseController:
    """
    Smooth mouse movement and click with random delay.
    """
    def __init__(self, smoothness=0.7):
        self.mouse = MouseControllerLib()
        self.smoothness = smoothness

    def move_to(self, x: int, y: int, duration=0.2):
        pyautogui.moveTo(x, y, duration=duration, tween=pyautogui.easeOutQuad)
        time.sleep(0.05)

    def click(self, button='left'):
        self.mouse.click(getattr(self.mouse.Button, button))

    def hold_and_release(self, hold_time: float):
        """Press left button, hold, then release."""
        self.mouse.press(self.mouse.Button.left)
        time.sleep(hold_time)
        self.mouse.release(self.mouse.Button.left)

    def bezier_move(self, start, end, steps=20):
        """Optional: Bezier curve movement."""
        pass
