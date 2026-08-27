# core/detection/classifier.py
import cv2
import numpy as np

class Classifier:
    """
    Shiny/Polluted/Normal classifier using pre-trained PyTorch model.
    """
    def __init__(self, model_loader, target_size=(64, 64)):
        self.model = model_loader.classifier_model
        self.target_size = target_size

    def classify(self, crop: np.ndarray) -> str:
        """
        Returns 'shiny', 'polluted', or 'normal'.
        """
        if self.model is None:
            return "normal"
        # Preprocess crop
        resized = cv2.resize(crop, self.target_size)
        # Normalize to [0,1] and convert to tensor (mock)
        # In real implementation: torch tensor -> model forward
        return "normal"  # placeholder
