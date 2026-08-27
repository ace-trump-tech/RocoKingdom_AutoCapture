# utils/geometry.py
import math
from typing import Tuple

def coordinate_transform(window_coords: Tuple[int, int], window_rect: Tuple[int, int, int, int]) -> Tuple[int, int]:
    """
    Transform coordinates relative to game window to absolute screen coordinates.
    
    :param window_coords: (x, y) relative to top-left of game window
    :param window_rect: (left, top, width, height) of the game window on screen
    :return: absolute screen coordinates (x_abs, y_abs)
    """
    left, top, _, _ = window_rect
    x_rel, y_rel = window_coords
    return (left + x_rel, top + y_rel)

def euclidean_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Calculate Euclidean distance between two points."""
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def point_in_rect(point: Tuple[float, float], rect: Tuple[float, float, float, float]) -> bool:
    """
    Check if point (x,y) lies inside rectangle (x, y, width, height).
    """
    px, py = point
    rx, ry, rw, rh = rect
    return rx <= px <= rx + rw and ry <= py <= ry + rh

def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp a value between min and max."""
    return max(min_val, min(value, max_val))
