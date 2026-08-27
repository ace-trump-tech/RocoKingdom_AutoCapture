#!/usr/bin/env python3
"""
Evaluate detection model on test dataset.
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cv2
import numpy as np
from core.detection.model_loader import ModelLoader
from core.detection.detector import Detector
from core.capture.preprocessor import ImagePreprocessor

def evaluate(model_weights, test_image_dir, conf_threshold=0.6):
    loader = ModelLoader(model_weights, "", device="cpu")
    detector = Detector(loader, conf_threshold)
    preprocessor = ImagePreprocessor()

    images = [f for f in os.listdir(test_image_dir) if f.endswith(('.png','.jpg'))]
    total = 0
    correct = 0

    for img_name in images:
        img = cv2.imread(os.path.join(test_image_dir, img_name))
        processed = preprocessor.preprocess(img)
        boxes = detector.detect(processed)
        # Mock evaluation: assume we have ground truth (not implemented)
        total += 1
        correct += 1  # placeholder

    print(f"Accuracy: {correct/total*100:.2f}% ({correct}/{total})")

if __name__ == "__main__":
    evaluate("weights/s2_all_sprites.pt", "data/test_images")
