import pytest
from PIL import Image

from minipixel.analysis.colors import (
    calculate_average_color, calculate_brightness, calculate_color_distance,
    count_unique_colors, find_dominant_color, get_color_distribution,
    get_color_histogram,
)


def test_color_statistics_have_expected_values() -> None:
    image = Image.new("RGB", (2, 1))
    image.putdata([(255, 0, 0), (0, 0, 255)])
    assert calculate_average_color(image) == (127.5, 0.0, 127.5)
    assert count_unique_colors(image) == 2
    assert get_color_histogram(image)["red"][255] == 1
    assert get_color_histogram(image)["blue"][255] == 1
    assert calculate_brightness(Image.new("L", (2, 2), 255)) == pytest.approx(255)
    assert calculate_color_distance((0, 0, 0), (3, 4, 0)) == 5
    assert sum(get_color_distribution(image).values()) == 1.0
    assert find_dominant_color(Image.new("RGB", (3, 2), (16, 32, 48))) == (24, 40, 56)


def test_color_validation() -> None:
    with pytest.raises(ValueError):
        calculate_color_distance((256, 0, 0), (0, 0, 0))
