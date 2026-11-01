"""Pixelwise image comparison metrics (not perceptual similarity metrics)."""

import numpy as np
from PIL import Image

from ..utils.validators import require_image


def compare_dimensions(image1: Image.Image, image2: Image.Image) -> bool:
    """Return whether both images have exactly the same width and height."""
    require_image(image1)
    require_image(image2)
    return image1.size == image2.size


def _matching_rgb_arrays(image1: Image.Image, image2: Image.Image) -> tuple[np.ndarray, np.ndarray]:
    require_image(image1)
    require_image(image2)
    if image1.size != image2.size:
        raise ValueError("images must have identical dimensions")
    return (
        np.asarray(image1.convert("RGB"), dtype=np.float32),
        np.asarray(image2.convert("RGB"), dtype=np.float32),
    )


def calculate_mean_absolute_error(image1: Image.Image, image2: Image.Image) -> float:
    """Mean absolute RGB-channel difference per channel, in the range 0..255."""
    first, second = _matching_rgb_arrays(image1, image2)
    return float(np.abs(first - second).mean())


def calculate_root_mean_square_error(image1: Image.Image, image2: Image.Image) -> float:
    """Root mean squared RGB-channel difference, in the range 0..255."""
    first, second = _matching_rgb_arrays(image1, image2)
    return float(np.sqrt(np.square(first - second).mean()))


def calculate_image_similarity(image1: Image.Image, image2: Image.Image) -> float:
    """Return ``1 - MAE/255`` for equal-sized RGB pixels, clamped to 0..1.

    This normalized pixelwise score does not establish perceptual equivalence.
    """
    return max(0.0, min(1.0, 1.0 - calculate_mean_absolute_error(image1, image2) / 255.0))


def are_images_identical(image1: Image.Image, image2: Image.Image) -> bool:
    """Return exact equality of dimensions and RGBA pixel data."""
    require_image(image1)
    require_image(image2)
    return image1.size == image2.size and image1.convert("RGBA").tobytes() == image2.convert("RGBA").tobytes()
