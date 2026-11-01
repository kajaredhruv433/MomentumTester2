"""Image cropping operations using Pillow's half-open box convention."""

from PIL import Image

from ..utils.validators import require_image, require_positive_int


def crop_image(
    image: Image.Image, left: int, top: int, right: int, bottom: int
) -> Image.Image:
    """Crop ``[left, right) x [top, bottom)``; bounds must be inside image."""
    require_image(image)
    coordinates = (left, top, right, bottom)
    if any(isinstance(value, bool) or not isinstance(value, int) for value in coordinates):
        raise TypeError("crop coordinates must be integers")
    if left < 0 or top < 0 or right > image.width or bottom > image.height:
        raise ValueError("crop coordinates must lie within the image")
    if right <= left or bottom <= top:
        raise ValueError("crop right/bottom must be greater than left/top")
    return image.crop((left, top, right, bottom))


def center_crop(image: Image.Image, width: int, height: int) -> Image.Image:
    """Crop the requested dimensions around the image center."""
    require_image(image)
    require_positive_int(width, "width")
    require_positive_int(height, "height")
    if width > image.width or height > image.height:
        raise ValueError("center crop cannot exceed the image dimensions")
    left = (image.width - width) // 2
    top = (image.height - height) // 2
    return crop_image(image, left, top, left + width, top + height)
