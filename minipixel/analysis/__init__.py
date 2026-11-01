"""Image color, quality, histogram, hash, and comparison analysis."""

from .colors import (
    calculate_average_color, calculate_brightness, calculate_color_distance,
    count_unique_colors, find_dominant_color, get_color_distribution,
    get_color_histogram,
)
from .comparison import (
    are_images_identical, calculate_image_similarity,
    calculate_mean_absolute_error, calculate_root_mean_square_error,
    compare_dimensions,
)
from .hashing import calculate_hash_distance, generate_image_hash

__all__ = [
    "calculate_average_color", "calculate_brightness", "calculate_color_distance",
    "count_unique_colors", "find_dominant_color", "get_color_distribution",
    "get_color_histogram", "compare_dimensions", "calculate_mean_absolute_error",
    "calculate_root_mean_square_error", "calculate_image_similarity",
    "generate_image_hash", "are_images_identical", "calculate_hash_distance",
]
