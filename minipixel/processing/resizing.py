"""Image resizing and padding."""

from PIL import Image

from ..utils.validators import require_image, require_positive_int

_RESAMPLING = Image.Resampling.LANCZOS


def resize_image(image: Image.Image, width: int, height: int) -> Image.Image:
    """Resize to exactly ``(width, height)`` using Lanczos resampling."""
    require_image(image)
    require_positive_int(width, "width")
    require_positive_int(height, "height")
    return image.resize((width, height), _RESAMPLING)


def resize_preserving_aspect_ratio(
    image: Image.Image, max_width: int, max_height: int
) -> Image.Image:
    """Fit within bounds without cropping or enlarging the original."""
    require_image(image)
    require_positive_int(max_width, "max_width")
    require_positive_int(max_height, "max_height")
    scale = min(max_width / image.width, max_height / image.height, 1.0)
    size = (max(1, round(image.width * scale)), max(1, round(image.height * scale)))
    return image.resize(size, _RESAMPLING)


def pad_image(
    image: Image.Image, width: int, height: int, color: object = 0
) -> Image.Image:
    """Center the image on a canvas at least as large as its current size."""
    require_image(image)
    require_positive_int(width, "width")
    require_positive_int(height, "height")
    if width < image.width or height < image.height:
        raise ValueError("padding dimensions cannot be smaller than the image")
    canvas = Image.new(image.mode, (width, height), color)
    canvas.paste(image, ((width - image.width) // 2, (height - image.height) // 2))
    return canvas


def thumbnail_image(image: Image.Image, max_size: int) -> Image.Image:
    """Return a copy fitted within a square bound, preserving aspect ratio."""
    require_image(image)
    require_positive_int(max_size, "max_size")
    result = image.copy()
    result.thumbnail((max_size, max_size), _RESAMPLING)
    return result
