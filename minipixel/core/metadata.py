"""Image metadata accessors."""

from PIL import Image


def _require_image(image: Image.Image) -> None:
    if not isinstance(image, Image.Image):
        raise TypeError("image must be a PIL.Image.Image")


def get_image_dimensions(image: Image.Image) -> tuple[int, int]:
    """Return image dimensions as ``(width, height)``."""
    _require_image(image)
    return image.size


def get_image_format(image: Image.Image) -> str | None:
    """Return the decoded source format, or ``None`` for an in-memory image."""
    _require_image(image)
    return image.format


def get_image_mode(image: Image.Image) -> str:
    """Return the Pillow mode, such as ``RGB`` or ``L``."""
    _require_image(image)
    return image.mode


def get_image_metadata(image: Image.Image) -> dict[str, object]:
    """Return a shallow copy of Pillow's metadata dictionary."""
    _require_image(image)
    return dict(image.info)
