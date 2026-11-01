from pathlib import Path

from PIL import Image

from minipixel.analysis.histogram import get_color_histogram
from minipixel.analysis.image_quality import calculate_brightness
from minipixel.main import main
from minipixel.utils.file_utils import make_output_path
from minipixel.utils.logger import get_logger


def test_helpers_and_cli_info(tmp_path: Path, capsys) -> None:
    path = tmp_path / "input.png"
    Image.new("RGB", (2, 1), (255, 0, 0)).save(path)
    assert get_color_histogram(Image.new("RGB", (1, 1), "red"))["red"][255] == 1
    assert calculate_brightness(Image.new("RGB", (1, 1), "white")) == 255
    assert make_output_path(path, "gray") == Path("output") / "input_gray.png"
    assert get_logger("minipixel.test").name == "minipixel.test"
    assert main(["info", str(path)]) == 0
    assert '"dimensions": [' in capsys.readouterr().out


def test_cli_transform_and_bad_input(tmp_path: Path, capsys) -> None:
    path = tmp_path / "source.png"
    output = tmp_path / "result.png"
    Image.new("RGB", (2, 1), (255, 0, 0)).save(path)
    assert main(["grayscale", str(path), str(output)]) == 0
    assert Image.open(output).mode == "L"
    assert main(["info", str(tmp_path / "missing.png")]) == 2
    assert "Error:" in capsys.readouterr().out
