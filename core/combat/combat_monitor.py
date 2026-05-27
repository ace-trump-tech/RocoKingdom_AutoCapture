# core/combat/combat_monitor.py
from core.capture.screen_grabber import ScreenGrabber
import time

class CombatMonitor:
    """
    Monitor if combat has ended (victory/defeat screen).
    """
    def __init__(self, grabber: ScreenGrabber):
        self.grabber = grabber

    def is_combat_over(self) -> bool:
        # Check for exit button or victory text (simplified)
        # Return True if combat ended
        return True  # placeholder

    def wait_for_combat_end(self, timeout=10):
        start = time.time()
        while time.time() - start < timeout:
            if self.is_combat_over():
                return True
            time.sleep(0.5)
        return False
