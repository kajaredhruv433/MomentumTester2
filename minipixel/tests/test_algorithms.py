import pytest
from PIL import Image

from minipixel.algorithms.geometry import (
    calculate_bounding_box, calculate_box_area, calculate_box_intersection,
    calculate_iou, normalize_coordinates,
)
from minipixel.algorithms.pixel_statistics import (
    calculate_region_average, get_pixel_value, set_pixel_value,
)
from minipixel.algorithms.similarity import calculate_similarity


def test_pixel_access_and_region_average() -> None:
    image = Image.new("RGB", (2, 2), (10, 20, 30))
    assert get_pixel_value(image, 1, 1) == (10, 20, 30)
    changed = set_pixel_value(image, 0, 0, (200, 150, 100))
    assert get_pixel_value(changed, 0, 0) == (200, 150, 100)
    assert get_pixel_value(image, 0, 0) == (10, 20, 30)
    assert calculate_region_average(image, 0, 0, 2, 2) == (10, 20, 30)
    assert calculate_region_average(Image.new("L", (1, 1), 128), 0, 0, 1, 1) == (128, 128, 128)
    with pytest.raises(ValueError):
        get_pixel_value(image, 2, 0)
    with pytest.raises(ValueError):
        calculate_region_average(image, 1, 1, 1, 2)


def test_geometry_intersection_iou_and_normalization() -> None:
    assert calculate_bounding_box([(2, 1), (-1, 5), (3, 4)]) == (-1.0, 1.0, 3.0, 5.0)
    assert calculate_box_area((0, 0, 4, 3)) == 12
    assert calculate_box_intersection((0, 0, 4, 4), (2, 1, 5, 3)) == (2, 1, 4, 3)
    assert calculate_iou((0, 0, 2, 2), (1, 1, 3, 3)) == pytest.approx(1 / 7)
    assert calculate_iou((0, 0, 0, 0), (1, 1, 1, 1)) == 0
    assert normalize_coordinates(5, 2, 10, 4) == (0.5, 0.5)
    assert normalize_coordinates(10, 4, 10, 4) == (1.0, 1.0)
    with pytest.raises(ValueError):
        calculate_bounding_box([])
    with pytest.raises(ValueError):
        normalize_coordinates(11, 0, 10, 10)


def test_similarity_matches_identical_images() -> None:
    image = Image.new("RGB", (2, 1), (12, 34, 56))
    assert calculate_similarity(image, image.copy()) == 1.0
