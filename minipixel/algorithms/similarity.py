"""Pixelwise similarity API shared with image comparison."""

from PIL import Image

from ..analysis.comparison import calculate_image_similarity


def calculate_similarity(image1: Image.Image, image2: Image.Image) -> float:
    """Return normalized pixelwise RGB similarity; this is not perceptual."""
    return calculate_image_similarity(image1, image2)


__all__ = ["calculate_similarity", "calculate_image_similarity"]
