from pathlib import Path

import pytest
from PIL import Image

from minipixel.core import (
    get_image_dimensions, get_image_format, get_image_metadata, get_image_mode,
    is_valid_image, load_image, save_image, validate_image,
)


def test_load_save_and_metadata(tmp_path: Path) -> None:
    source = Image.new("RGB", (3, 2), (12, 34, 56))
    path = tmp_path / "small.png"
    save_image(source, path)
    loaded = load_image(path)
    assert get_image_dimensions(loaded) == (3, 2)
    assert get_image_format(loaded) == "PNG"
    assert get_image_mode(loaded) == "RGB"
    assert get_image_metadata(loaded) == {}
    assert loaded.getpixel((1, 1)) == (12, 34, 56)
    assert validate_image(path) and is_valid_image(path)


def test_invalid_files_and_bad_arguments(tmp_path: Path) -> None:
    missing = tmp_path / "missing.png"
    broken = tmp_path / "broken.png"
    broken.write_text("not an image", encoding="utf-8")
    assert not validate_image(missing)
    assert not is_valid_image(broken)
    with pytest.raises(FileNotFoundError):
        load_image(missing)
    with pytest.raises(ValueError):
        load_image(broken)
    with pytest.raises(TypeError):
        load_image(42)  # type: ignore[arg-type]
