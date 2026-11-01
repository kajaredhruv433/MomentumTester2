"""Image saving helpers."""

from pathlib import Path
from typing import Union

from PIL import Image

PathLike = Union[str, Path]


def save_image(image: Image.Image, path: PathLike, image_format: str | None = None) -> Path:
    """Save an image to ``path`` and return the destination path.

    Parent directories are not created implicitly. An optional format is passed
    to Pillow and should be a supported format name such as ``"PNG"``.
    """
    if not isinstance(image, Image.Image):
        raise TypeError("image must be a PIL.Image.Image")
    if not isinstance(path, (str, Path)):
        raise TypeError("path must be a string or pathlib.Path")
    destination = Path(path)
    if image_format is None:
        image.save(destination)
    else:
        image.save(destination, format=image_format)
    return destination
