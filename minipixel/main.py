"""Command-line interface for MiniPixel."""

import argparse
import json
from pathlib import Path
import sys
from typing import Callable

from PIL import Image

# Allow ``python main.py`` from the project directory as well as
# ``python minipixel/main.py`` from its parent directory.
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from minipixel.analysis.colors import (
    calculate_average_color, calculate_brightness, count_unique_colors,
    find_dominant_color, get_color_distribution, get_color_histogram,
)
from minipixel.analysis.comparison import (
    calculate_image_similarity, calculate_mean_absolute_error,
    calculate_root_mean_square_error, compare_dimensions,
)
from minipixel.core import load_image, save_image
from minipixel.processing.filters import (
    adjust_brightness, apply_blur, convert_to_grayscale, invert_colors,
    rotate_image,
)
from minipixel.processing.resizing import resize_image
from minipixel.utils.file_utils import make_output_path


def _output_path(source: str, explicit: str | None, operation: str) -> Path:
    return Path(explicit) if explicit else make_output_path(source, operation)


def _save_result(image: Image.Image, source: str, explicit: str | None, operation: str) -> Path:
    destination = _output_path(source, explicit, operation)
    destination.parent.mkdir(parents=True, exist_ok=True)
    save_image(image, destination)
    print(f"Saved {destination}")
    return destination


def _add_output_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("output", nargs="?", help="output image path (default: output/<name>_<operation>.<ext>)")


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI parser."""
    parser = argparse.ArgumentParser(description="Inspect and transform images with MiniPixel.")
    commands = parser.add_subparsers(dest="command", required=True)

    info = commands.add_parser("info", help="show image dimensions, mode, format, and metadata")
    info.add_argument("image")

    for name in ("grayscale", "invert"):
        command = commands.add_parser(name, help=f"write a {name} copy")
        command.add_argument("image")
        _add_output_argument(command)

    resize = commands.add_parser("resize", help="resize to exact dimensions")
    resize.add_argument("image")
    resize.add_argument("width", type=int)
    resize.add_argument("height", type=int)
    resize.add_argument("output", nargs="?")

    rotate = commands.add_parser("rotate", help="rotate counter-clockwise in degrees")
    rotate.add_argument("image")
    rotate.add_argument("angle", type=float)
    rotate.add_argument("output", nargs="?")

    blur = commands.add_parser("blur", help="apply Gaussian blur")
    blur.add_argument("image")
    blur.add_argument("radius", type=float)
    blur.add_argument("output", nargs="?")

    brightness = commands.add_parser("brightness", help="adjust brightness")
    brightness.add_argument("image")
    brightness.add_argument("factor", type=float)
    brightness.add_argument("output", nargs="?")

    colors = commands.add_parser("colors", help="summarize image colors")
    colors.add_argument("image")
    compare = commands.add_parser("compare", help="compare two same-size images pixelwise")
    compare.add_argument("image1")
    compare.add_argument("image2")
    histogram = commands.add_parser("histogram", help="print the per-channel intensity histogram")
    histogram.add_argument("image")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CLI and return a process status code."""
    args = build_parser().parse_args(argv)
    try:
        if args.command == "info":
            image = load_image(args.image)
            print(json.dumps({
                "path": str(args.image),
                "dimensions": image.size,
                "format": image.format,
                "mode": image.mode,
                "metadata": image.info,
            }, indent=2, default=str))
        elif args.command in ("grayscale", "invert"):
            image = load_image(args.image)
            operation: Callable[[Image.Image], Image.Image] = (
                convert_to_grayscale if args.command == "grayscale" else invert_colors
            )
            _save_result(operation(image), args.image, args.output, args.command)
        elif args.command == "resize":
            _save_result(
                resize_image(load_image(args.image), args.width, args.height),
                args.image, args.output, "resize",
            )
        elif args.command == "rotate":
            _save_result(
                rotate_image(load_image(args.image), args.angle),
                args.image, args.output, "rotate",
            )
        elif args.command == "blur":
            _save_result(
                apply_blur(load_image(args.image), args.radius),
                args.image, args.output, "blur",
            )
        elif args.command == "brightness":
            _save_result(
                adjust_brightness(load_image(args.image), args.factor),
                args.image, args.output, "brightness",
            )
        elif args.command == "colors":
            image = load_image(args.image)
            print(json.dumps({
                "average_rgb": calculate_average_color(image),
                "dominant_rgb_approx": find_dominant_color(image),
                "brightness": calculate_brightness(image),
                "unique_rgb_colors": count_unique_colors(image),
                "dominant_channel_distribution": get_color_distribution(image),
            }, indent=2))
        elif args.command == "compare":
            first, second = load_image(args.image1), load_image(args.image2)
            dimensions_match = compare_dimensions(first, second)
            result: dict[str, object] = {"same_dimensions": dimensions_match}
            if dimensions_match:
                result.update({
                    "mean_absolute_error": calculate_mean_absolute_error(first, second),
                    "root_mean_square_error": calculate_root_mean_square_error(first, second),
                    "pixel_similarity": calculate_image_similarity(first, second),
                })
            print(json.dumps(result, indent=2))
        elif args.command == "histogram":
            print(json.dumps(get_color_histogram(load_image(args.image)), indent=2))
        return 0
    except (OSError, ValueError, TypeError) as exc:
        print(f"Error: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
