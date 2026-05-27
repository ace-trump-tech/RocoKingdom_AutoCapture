# core/capture/preprocessor.py
import cv2
import numpy as np

class ImagePreprocessor:
    """
    Preprocess captured image: resize, color conversion, denoise.
    """
    def __init__(self, target_size: tuple = (640, 640)):
        self.target_size = target_size

    def preprocess(self, image: np.ndarray) -> np.ndarray:
        """
        Resize to model input size, convert to RGB, apply light denoise.
        """
        if image is None:
            return None
        # Convert BGR to RGB
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Resize
        resized = cv2.resize(rgb, self.target_size, interpolation=cv2.INTER_LINEAR)
        # Optional: Gaussian blur for noise reduction
        # resized = cv2.GaussianBlur(resized, (3,3), 0)
        return resized

    def get_original_size(self, image: np.ndarray) -> tuple:
        return (image.shape[1], image.shape[0])
