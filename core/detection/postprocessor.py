# core/detection/postprocessor.py
from typing import List, Tuple
import numpy as np

class PostProcessor:
    """
    Sort detected sprites by priority and select target.
    """
    def __init__(self, priority_map: dict):
        """
        priority_map = {'shiny':1, 'polluted':2, 'high_exp':3, 'normal':4}
        """
        self.priority = priority_map

    def select_target(self, detections: List[Tuple[np.ndarray, str, float]]):
        """
        Input: list of (bounding_box, class_label, confidence)
        Output: best target box or None
        """
        if not detections:
            return None
        # Sort by priority value (lower is better)
        detections.sort(key=lambda x: self.priority.get(x[1], 99))
        return detections[0][0]  # return box of highest priority
