# core/detection/model_loader.py
import torch
from ultralytics import YOLO
from pathlib import Path

class ModelLoader:
    """Load YOLO detection model and PyTorch classifier model."""
    def __init__(self, detection_weight: str, classifier_weight: str, device: str = "cuda"):
        self.device = device if torch.cuda.is_available() else "cpu"
        self.detection_model = YOLO(detection_weight)
        self.classifier_model = None
        if Path(classifier_weight).exists():
            self.classifier_model = torch.load(classifier_weight, map_location=self.device)
            self.classifier_model.eval()
        else:
            print("Warning: classifier weight not found, shiny detection disabled.")

    def detect(self, image):
        """Run YOLO detection, return list of boxes."""
        results = self.detection_model(image, verbose=False)
        return results[0].boxes

    def classify_shiny(self, crop):
        """Classify if a sprite crop is shiny/polluted/normal."""
        if self.classifier_model is None:
            return "normal"  # fallback
        # Preprocess crop, run inference
        # (simplified; actual implementation would resize & normalize)
        return "normal"
