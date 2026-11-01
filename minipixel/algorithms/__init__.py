"""Pixel-level statistics and geometry algorithms."""

from .geometry import (
    calculate_box_area, calculate_box_intersection, calculate_bounding_box,
    calculate_iou, normalize_coordinates,
)
from .pixel_statistics import (
    calculate_region_average, get_pixel_value, set_pixel_value,
)
from .similarity import calculate_similarity

__all__ = [
    "get_pixel_value", "set_pixel_value", "calculate_region_average",
    "calculate_bounding_box", "calculate_box_area",
    "calculate_box_intersection", "calculate_iou", "normalize_coordinates",
    "calculate_similarity",
]
