# core/capture/region_selector.py
import cv2
import numpy as np
from typing import Tuple, Optional

class RegionSelector:
    """
    Interactive tool to select game window region.
    """
    @staticmethod
    def select_region(screen: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """
        Display screen and let user draw rectangle.
        Returns (left, top, width, height) or None if canceled.
        """
        clone = screen.copy()
        roi = cv2.selectROI("Select Game Window", clone, False, False)
        cv2.destroyAllWindows()
        if roi == (0,0,0,0):
            return None
        return (int(roi[0]), int(roi[1]), int(roi[2]), int(roi[3]))
