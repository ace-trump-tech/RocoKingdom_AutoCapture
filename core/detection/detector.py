# core/detection/detector.py
import numpy as np
from .model_loader import ModelLoader

class Detector:
    """Interface for running detection and returning bounding boxes."""
    def __init__(self, model_loader: ModelLoader, conf_threshold: float = 0.6):
        self.model = model_loader
        self.conf_threshold = conf_threshold

    def detect(self, image: np.ndarray):
        boxes = self.model.detect(image)
        # Filter by confidence
        filtered = []
        for box in boxes:
            if box.conf[0] >= self.conf_threshold:
                filtered.append(box)
        return filtered
