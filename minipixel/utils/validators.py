"""Reusable validation helpers."""

import math
from numbers import Real


def require_positive_int(value: int, name: str) -> None:
    """Require a positive integer, explicitly excluding booleans."""
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} must be a positive integer")


def require_nonnegative_real(value: Real, name: str) -> None:
    """Require a finite, non-negative real number."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number")
    if not math.isfinite(float(value)) or value < 0:
        raise ValueError(f"{name} must be finite and non-negative")


def require_image(image: object) -> None:
    """Require a Pillow image without importing Pillow at module load time."""
    from PIL import Image

    if not isinstance(image, Image.Image):
        raise TypeError("image must be a PIL.Image.Image")
