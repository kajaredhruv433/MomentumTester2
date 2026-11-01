import pytest
from PIL import Image

from minipixel.analysis.comparison import (
    are_images_identical, calculate_image_similarity,
    calculate_mean_absolute_error, calculate_root_mean_square_error,
    compare_dimensions,
)
from minipixel.analysis.hashing import calculate_hash_distance, generate_image_hash


def test_comparison_metrics() -> None:
    black = Image.new("RGB", (2, 2), (0, 0, 0))
    white = Image.new("RGB", (2, 2), (255, 255, 255))
    assert compare_dimensions(black, white)
    assert calculate_mean_absolute_error(black, white) == 255
    assert calculate_root_mean_square_error(black, white) == 255
    assert calculate_image_similarity(black, white) == 0
    assert are_images_identical(black, black.copy())
    assert not are_images_identical(black, white)
    assert not compare_dimensions(black, Image.new("RGB", (1, 2)))
    with pytest.raises(ValueError):
        calculate_mean_absolute_error(black, Image.new("RGB", (1, 2)))


def test_hashes_and_distances_are_deterministic() -> None:
    image = Image.new("L", (10, 10), 80)
    hashed = generate_image_hash(image)
    assert len(hashed) == 16
    assert generate_image_hash(image) == hashed
    assert calculate_hash_distance("0f", "00") == 4
    with pytest.raises(ValueError):
        calculate_hash_distance("0", "00")
    with pytest.raises(ValueError):
        calculate_hash_distance("zz", "aa")
