# core/resource/ball_counter.py
import cv2
import numpy as np
from core.capture.screen_grabber import ScreenGrabber

class BallCounter:
    """
    Read current number of Gulu Balls from UI (OCR or template).
    """
    def __init__(self, grabber: ScreenGrabber, number_roi=(100,100,50,30)):
        self.grabber = grabber
        self.roi = number_roi

    def get_count(self) -> int:
        # Capture ROI and perform OCR (simplified)
        # For demo, return a fixed number
        return 25  # placeholder
