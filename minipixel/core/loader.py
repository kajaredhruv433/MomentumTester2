"""Image file loading."""

from pathlib import Path
from typing import Union

from PIL import Image, UnidentifiedImageError

PathLike = Union[str, Path]


def load_image(path: PathLike) -> Image.Image:
    """Load and fully decode an image, leaving its file handle closed.

    Missing files raise ``FileNotFoundError``; unsupported or corrupt images
    raise ``ValueError`` with the original Pillow exception chained.
    """
    if not isinstance(path, (str, Path)):
        raise TypeError("path must be a string or pathlib.Path")
    try:
        with Image.open(path) as image:
            image.load()
            loaded = image.copy()
            loaded.format = image.format
            return loaded
    except (UnidentifiedImageError, OSError) as exc:
        if isinstance(exc, FileNotFoundError):
            raise
        raise ValueError(f"Unable to load image at {path!s}: {exc}") from exc
