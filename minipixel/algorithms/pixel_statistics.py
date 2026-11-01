"""Pixel access and rectangular region statistics."""

import numpy as np
from PIL import Image

from ..utils.validators import require_image


def _validate_pixel_coordinate(value: int, limit: int, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if not 0 <= value < limit:
        raise ValueError(f"{name} must be within the image bounds")


def get_pixel_value(image: Image.Image, x: int, y: int) -> int | tuple[int, ...]:
    """Return a pixel at integer ``(x, y)``; origin is top-left."""
    require_image(image)
    _validate_pixel_coordinate(x, image.width, "x")
    _validate_pixel_coordinate(y, image.height, "y")
    value = image.getpixel((x, y))
    return value


def set_pixel_value(
    image: Image.Image, x: int, y: int, color: int | tuple[int, ...]
) -> Image.Image:
    """Return a modified copy with one pixel set; the input is not mutated."""
    require_image(image)
    _validate_pixel_coordinate(x, image.width, "x")
    _validate_pixel_coordinate(y, image.height, "y")
    result = image.copy()
    try:
        result.putpixel((x, y), color)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"color is invalid for image mode {image.mode}") from exc
    return result


def calculate_region_average(
    image: Image.Image, x1: int, y1: int, x2: int, y2: int
) -> tuple[float, float, float]:
    """Mean RGB of the non-empty half-open region ``[x1,x2) x [y1,y2)``."""
    require_image(image)
    values = (x1, y1, x2, y2)
    if any(isinstance(value, bool) or not isinstance(value, int) for value in values):
        raise TypeError("region coordinates must be integers")
    if x1 < 0 or y1 < 0 or x2 > image.width or y2 > image.height:
        raise ValueError("region coordinates must lie within the image")
    if x2 <= x1 or y2 <= y1:
        raise ValueError("region must have positive width and height")
    region = np.asarray(image.convert("RGB").crop((x1, y1, x2, y2)), dtype=np.float64)
    return tuple(float(value) for value in region.mean(axis=(0, 1)))
