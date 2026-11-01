"""Color statistics. Images are processed as RGB unless stated otherwise."""

import numpy as np
from PIL import Image

from ..config import DEFAULT_DOMINANT_COLOR_BITS
from ..utils.validators import require_image


def _rgb_array(image: Image.Image) -> np.ndarray:
    require_image(image)
    return np.asarray(image.convert("RGB"), dtype=np.uint8)


def calculate_average_color(image: Image.Image) -> tuple[float, float, float]:
    """Return mean red, green, and blue channel values in the 0..255 range."""
    return tuple(float(value) for value in _rgb_array(image).mean(axis=(0, 1)))


def find_dominant_color(image: Image.Image) -> tuple[int, int, int]:
    """Return the center of the most populated 4-bit-per-channel RGB bin.

    Quantization bounds working memory while making the meaning of this
    lightweight dominant-color estimate explicit.
    """
    array = _rgb_array(image)
    bits = DEFAULT_DOMINANT_COLOR_BITS
    shift = 8 - bits
    bins = (array >> shift).astype(np.int32)
    indexes = bins[:, :, 0] * (1 << (2 * bits)) + bins[:, :, 1] * (1 << bits) + bins[:, :, 2]
    counts = np.bincount(indexes.ravel(), minlength=1 << (3 * bits))
    red_bin, remainder = divmod(int(counts.argmax()), 1 << (2 * bits))
    green_bin, blue_bin = divmod(remainder, 1 << bits)
    center_offset = (1 << shift) // 2
    return tuple(min(255, channel * (1 << shift) + center_offset)
                 for channel in (red_bin, green_bin, blue_bin))


def get_color_histogram(image: Image.Image) -> dict[str, list[int]]:
    """Return 256-bin intensity counts separately for each RGB channel."""
    array = _rgb_array(image)
    labels = ("red", "green", "blue")
    return {
        label: np.bincount(array[:, :, index].ravel(), minlength=256).astype(int).tolist()
        for index, label in enumerate(labels)
    }


def count_unique_colors(image: Image.Image) -> int:
    """Count unique RGB pixel values, ignoring alpha and non-RGB metadata."""
    array = _rgb_array(image)
    return int(np.unique(array.reshape(-1, 3), axis=0).shape[0])


def calculate_brightness(image: Image.Image) -> float:
    """Return mean Rec. 601 luma (0 black through 255 white)."""
    array = _rgb_array(image).astype(np.float32)
    luma = array[:, :, 0] * 0.299 + array[:, :, 1] * 0.587 + array[:, :, 2] * 0.114
    return float(luma.mean())


def calculate_color_distance(
    color1: tuple[int, int, int], color2: tuple[int, int, int]
) -> float:
    """Return Euclidean distance between two RGB triples (range 0..441.67)."""
    for name, color in (("color1", color1), ("color2", color2)):
        if not isinstance(color, (tuple, list)) or len(color) != 3:
            raise ValueError(f"{name} must contain exactly three RGB values")
        if any(isinstance(value, bool) or not isinstance(value, (int, float))
               or not np.isfinite(value) or not 0 <= value <= 255 for value in color):
            raise ValueError(f"{name} values must be finite numbers from 0 to 255")
    return float(np.linalg.norm(np.asarray(color1, dtype=float) - np.asarray(color2, dtype=float)))


def get_color_distribution(image: Image.Image) -> dict[str, float]:
    """Return normalized proportions of red-, green-, and blue-dominant pixels."""
    array = _rgb_array(image).astype(np.int16)
    labels = np.argmax(array, axis=2)
    total = labels.size
    return {
        "red": float(np.count_nonzero(labels == 0) / total),
        "green": float(np.count_nonzero(labels == 1) / total),
        "blue": float(np.count_nonzero(labels == 2) / total),
    }
