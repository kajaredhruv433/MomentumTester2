import pytest
from PIL import Image

from minipixel.processing.filters import (
    adjust_brightness, adjust_contrast, apply_blur, convert_to_grayscale,
    flip_horizontal, flip_vertical, invert_colors, rotate_image, sharpen_image,
)


def test_filters_pixel_results_and_modes() -> None:
    image = Image.new("RGB", (2, 1))
    image.putdata([(10, 20, 30), (200, 100, 50)])
    assert convert_to_grayscale(image).mode == "L"
    assert adjust_brightness(image, 0).getpixel((0, 0)) == (0, 0, 0)
    assert adjust_brightness(image, 1).getpixel((0, 0)) == (10, 20, 30)
    assert adjust_contrast(image, 1).tobytes() == image.tobytes()
    assert flip_horizontal(image).getpixel((0, 0)) == (200, 100, 50)
    assert flip_vertical(image).size == image.size
    assert rotate_image(image, 90).size == (1, 2)
    assert invert_colors(image).getpixel((0, 0)) == (245, 235, 225)
    assert apply_blur(image, 0).tobytes() == image.tobytes()
    assert sharpen_image(image).size == image.size


def test_filter_boundaries_and_alpha() -> None:
    rgba = Image.new("RGBA", (1, 1), (10, 20, 30, 77))
    assert invert_colors(rgba).getpixel((0, 0)) == (245, 235, 225, 77)
    assert invert_colors(Image.new("1", (1, 1), 1)).getpixel((0, 0)) == 0
    cmyk = invert_colors(Image.new("CMYK", (1, 1), (10, 20, 30, 40)))
    assert cmyk.mode == "RGB"
    with pytest.raises(ValueError):
        adjust_brightness(rgba, -1)
    with pytest.raises(ValueError):
        apply_blur(rgba, -0.5)
