# core/tracking/predictor.py
import numpy as np
from collections import deque

class TrajectoryPredictor:
    """
    Predict future position based on historical positions.
    """
    def __init__(self, history_len=5):
        self.history = deque(maxlen=history_len)

    def update(self, position: tuple):
        self.history.append(position)

    def predict(self, steps_ahead=1) -> tuple:
        if len(self.history) < 2:
            return self.history[-1] if self.history else (0,0)
        # Simple linear extrapolation
        dx = self.history[-1][0] - self.history[-2][0]
        dy = self.history[-1][1] - self.history[-2][1]
        last = self.history[-1]
        return (last[0] + dx * steps_ahead, last[1] + dy * steps_ahead)
