"""Image file validation."""

from pathlib import Path
from typing import Union

from PIL import Image, UnidentifiedImageError

from ..config import SUPPORTED_IMAGE_FORMATS

PathLike = Union[str, Path]


def validate_image(path: PathLike) -> bool:
    """Return whether ``path`` exists and is a supported, decodable image."""
    if not isinstance(path, (str, Path)):
        raise TypeError("path must be a string or pathlib.Path")
    try:
        with Image.open(path) as image:
            if image.format not in SUPPORTED_IMAGE_FORMATS:
                return False
            image.verify()
        return True
    except (OSError, UnidentifiedImageError, ValueError):
        return False


def is_valid_image(path: PathLike) -> bool:
    """Alias for :func:`validate_image`."""
    return validate_image(path)
