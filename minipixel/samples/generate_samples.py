"""Generate deterministic, small synthetic MiniPixel sample images."""

import random
from pathlib import Path

from PIL import Image, ImageDraw


OUTPUT_DIR = Path(__file__).resolve().parent
SIZE = 256


def generate_samples(output_dir: Path = OUTPUT_DIR) -> list[Path]:
    """Generate five 256x256 PNG examples and return their paths."""
    output_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []

    landscape = Image.new("RGB", (SIZE, SIZE), (110, 190, 235))
    draw = ImageDraw.Draw(landscape)
    draw.ellipse((174, 24, 224, 74), fill=(255, 220, 80))
    draw.polygon([(0, 170), (70, 75), (145, 170)], fill=(77, 130, 96))
    draw.polygon([(75, 170), (170, 95), (256, 170)], fill=(65, 110, 85))
    draw.rectangle((0, 170, SIZE, SIZE), fill=(74, 155, 80))
    draw.polygon([(106, 256), (133, 171), (151, 171), (196, 256)], fill=(190, 170, 120))
    paths.append(_save(landscape, output_dir / "landscape.png"))

    shapes = Image.new("RGB", (SIZE, SIZE), (245, 245, 245))
    draw = ImageDraw.Draw(shapes)
    draw.rectangle((20, 20, 105, 95), fill=(230, 60, 55))
    draw.ellipse((142, 20, 232, 110), fill=(50, 150, 230))
    draw.polygon([(128, 128), (220, 230), (35, 230)], fill=(65, 185, 105))
    draw.rectangle((104, 35, 142, 222), fill=(235, 190, 45))
    paths.append(_save(shapes, output_dir / "shapes.png"))

    gradient = Image.new("RGB", (SIZE, SIZE))
    pixels = gradient.load()
    for y in range(SIZE):
        for x in range(SIZE):
            pixels[x, y] = (x, y, (x + y) // 2)
    paths.append(_save(gradient, output_dir / "gradient.png"))

    checkerboard = Image.new("RGB", (SIZE, SIZE))
    pixels = checkerboard.load()
    tile = 32
    for y in range(SIZE):
        for x in range(SIZE):
            value = 255 if (x // tile + y // tile) % 2 else 0
            pixels[x, y] = (value, value, value)
    paths.append(_save(checkerboard, output_dir / "checkerboard.png"))

    generator = random.Random(20240517)
    noise = Image.new("RGB", (SIZE, SIZE))
    noise.putdata([
        (generator.randrange(256), generator.randrange(256), generator.randrange(256))
        for _ in range(SIZE * SIZE)
    ])
    paths.append(_save(noise, output_dir / "noise.png"))
    return paths


def _save(image: Image.Image, path: Path) -> Path:
    image.save(path, format="PNG", optimize=True)
    return path


if __name__ == "__main__":
    for generated_path in generate_samples():
        print(f"Generated {generated_path}")
