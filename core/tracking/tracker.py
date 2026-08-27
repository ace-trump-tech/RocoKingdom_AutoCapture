# core/tracking/tracker.py
import numpy as np
from filterpy.kalman import KalmanFilter

class TargetTracker:
    """
    Kalman filter for smooth target tracking.
    """
    def __init__(self):
        self.kf = KalmanFilter(dim_x=4, dim_z=2)
        self.kf.F = np.array([[1,0,1,0],
                              [0,1,0,1],
                              [0,0,1,0],
                              [0,0,0,1]])
        self.kf.H = np.array([[1,0,0,0],
                              [0,1,0,0]])
        self.kf.P *= 1000
        self.kf.R = 5
        self.kf.Q = 0.05
        self.initialized = False

    def update(self, measurement: np.ndarray) -> np.ndarray:
        """measurement: [x, y] center of target."""
        if not self.initialized:
            self.kf.x[:2] = measurement
            self.initialized = True
        else:
            self.kf.predict()
            self.kf.update(measurement)
        return self.kf.x[:2]
