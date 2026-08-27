# core/capture/screen_grabber.py
import mss
import numpy as np
from typing import Tuple, Optional

class ScreenGrabber:
    """
    Captures game window or full screen using mss.
    """
    def __init__(self, region: Optional[Tuple[int, int, int, int]] = None):
        """
        :param region: (left, top, width, height) or None for full screen
        """
        self.sct = mss.mss()
        self.region = region
        if region is not None:
            self.monitor = {"left": region[0], "top": region[1],
                            "width": region[2], "height": region[3]}
        else:
            self.monitor = self.sct.monitors[1]  # primary monitor

    def capture(self) -> np.ndarray:
        """Return BGR image as numpy array."""
        img = self.sct.grab(self.monitor)
        return np.array(img)[:, :, :3]  # BGRA -> BGR

    def set_region(self, region: Tuple[int, int, int, int]):
        self.region = region
        self.monitor = {"left": region[0], "top": region[1],
                        "width": region[2], "height": region[3]}
