"""Deterministic average image hashing."""

from PIL import Image, ImageOps
import numpy as np

from ..config import DEFAULT_HASH_SIZE
from ..utils.validators import require_image, require_positive_int


def generate_image_hash(image: Image.Image, hash_size: int = DEFAULT_HASH_SIZE) -> str:
    """Create an average hash as a fixed-width lowercase hexadecimal string.

    The image is converted to grayscale, reduced to ``hash_size`` squared
    samples, and each sample is compared with their arithmetic mean.
    """
    require_image(image)
    require_positive_int(hash_size, "hash_size")
    sample = ImageOps.grayscale(image).resize((hash_size, hash_size), Image.Resampling.LANCZOS)
    pixels = np.asarray(sample, dtype=np.uint8).ravel()
    mean = float(pixels.mean())
    value = 0
    for pixel in pixels:
        value = (value << 1) | (int(pixel) >= mean)
    digits = (hash_size * hash_size + 3) // 4
    return f"{value:0{digits}x}"


def calculate_hash_distance(hash1: str, hash2: str) -> int:
    """Return Hamming distance between equal-length hexadecimal hashes."""
    if not isinstance(hash1, str) or not isinstance(hash2, str):
        raise TypeError("hashes must be strings")
    try:
        first, second = int(hash1, 16), int(hash2, 16)
    except ValueError as exc:
        raise ValueError("hashes must contain only hexadecimal digits") from exc
    if not hash1 or len(hash1) != len(hash2):
        raise ValueError("hashes must be non-empty and have equal length")
    return (first ^ second).bit_count()
