"""Axis-aligned bounding-box utilities.

Boxes use ``(x_min, y_min, x_max, y_max)`` coordinates; right and bottom are
exclusive for area calculations, as in common continuous-coordinate geometry.
"""

import math
from numbers import Real
from typing import Iterable

Box = tuple[float, float, float, float]


def _finite_number(value: object, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    return result


def _validate_box(box: tuple[float, float, float, float]) -> Box:
    if not isinstance(box, (tuple, list)) or len(box) != 4:
        raise ValueError("box must contain (x_min, y_min, x_max, y_max)")
    x1, y1, x2, y2 = (_finite_number(value, "box coordinate") for value in box)
    if x2 < x1 or y2 < y1:
        raise ValueError("box maximum coordinates cannot precede minimum coordinates")
    return x1, y1, x2, y2


def calculate_bounding_box(points: Iterable[tuple[Real, Real]]) -> Box:
    """Return min/max extents for non-empty ``(x, y)`` points."""
    if points is None:
        raise TypeError("points cannot be None")
    coordinates: list[tuple[float, float]] = []
    for point in points:
        if not isinstance(point, (tuple, list)) or len(point) != 2:
            raise ValueError("each point must contain exactly (x, y)")
        coordinates.append((_finite_number(point[0], "x"), _finite_number(point[1], "y")))
    if not coordinates:
        raise ValueError("points cannot be empty")
    xs, ys = zip(*coordinates)
    return min(xs), min(ys), max(xs), max(ys)


def calculate_box_area(box: tuple[float, float, float, float]) -> float:
    """Return non-negative width times height of a box."""
    x1, y1, x2, y2 = _validate_box(box)
    return (x2 - x1) * (y2 - y1)


def calculate_box_intersection(
    box1: tuple[float, float, float, float],
    box2: tuple[float, float, float, float],
) -> Box:
    """Return intersection extents; disjoint boxes have zero-area extents."""
    x1, y1, x2, y2 = _validate_box(box1)
    a1, b1, a2, b2 = _validate_box(box2)
    left, top = max(x1, a1), max(y1, b1)
    return left, top, max(left, min(x2, a2)), max(top, min(y2, b2))


def calculate_iou(
    box1: tuple[float, float, float, float],
    box2: tuple[float, float, float, float],
) -> float:
    """Return intersection over union, or 0 for zero-area union."""
    intersection = calculate_box_area(calculate_box_intersection(box1, box2))
    union = calculate_box_area(box1) + calculate_box_area(box2) - intersection
    return intersection / union if union else 0.0


def normalize_coordinates(x: Real, y: Real, width: Real, height: Real) -> tuple[float, float]:
    """Normalize edge coordinates by dimensions; coordinates may equal bounds."""
    x_value = _finite_number(x, "x")
    y_value = _finite_number(y, "y")
    width_value = _finite_number(width, "width")
    height_value = _finite_number(height, "height")
    if width_value <= 0 or height_value <= 0:
        raise ValueError("width and height must be positive")
    if not 0 <= x_value <= width_value or not 0 <= y_value <= height_value:
        raise ValueError("coordinates must be within the supplied dimensions")
    return x_value / width_value, y_value / height_value
