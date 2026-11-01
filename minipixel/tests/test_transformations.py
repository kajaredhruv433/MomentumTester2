import pytest
from PIL import Image

from minipixel.processing.cropping import center_crop, crop_image
from minipixel.processing.resizing import (
    pad_image, resize_image, resize_preserving_aspect_ratio, thumbnail_image,
)


def test_resize_preserves_aspect_and_thumbnail() -> None:
    image = Image.new("RGB", (8, 4), "red")
    assert resize_image(image, 3, 7).size == (3, 7)
    assert resize_preserving_aspect_ratio(image, 4, 4).size == (4, 2)
    assert resize_preserving_aspect_ratio(image, 20, 20).size == (8, 4)
    assert thumbnail_image(image, 3).size == (3, 2)
    with pytest.raises(ValueError):
        resize_image(image, 0, 2)


def test_crop_and_padding_pixel_values() -> None:
    image = Image.new("RGB", (4, 3), "red")
    crop = crop_image(image, 1, 1, 3, 3)
    assert crop.size == (2, 2)
    assert crop.getpixel((0, 0)) == (255, 0, 0)
    assert center_crop(image, 2, 1).size == (2, 1)
    padded = pad_image(image, 6, 5, "blue")
    assert padded.getpixel((0, 0)) == (0, 0, 255)
    assert padded.getpixel((1, 1)) == (255, 0, 0)
    with pytest.raises(ValueError):
        crop_image(image, 0, 0, 5, 2)
    with pytest.raises(ValueError):
        center_crop(image, 5, 2)
    with pytest.raises(ValueError):
        pad_image(image, 3, 3)
