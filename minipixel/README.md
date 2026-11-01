# MiniPixel

MiniPixel is a small Python 3.10+ image toolkit built on Pillow and NumPy. It
provides deterministic image I/O, transformations, color statistics,
pixelwise comparisons, simple image hashing, and geometry helpers. It does not
use machine-learning models, external services, or network access at runtime.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install pytest
python samples\generate_samples.py
python -m pytest
```

`requirements.txt` contains only the two runtime dependencies. Install pytest
separately for development and testing.

## CLI

Run commands from this directory:

```text
python main.py info samples/landscape.png
python main.py grayscale samples/landscape.png
python main.py resize samples/landscape.png 300 200
python main.py rotate samples/landscape.png 90
python main.py colors samples/landscape.png
python main.py compare samples/landscape.png samples/shapes.png
python main.py histogram samples/landscape.png
python main.py invert samples/landscape.png
python main.py blur samples/landscape.png 2
```

Transformations accept an optional final output path. By default, files are
written under `output/` with an operation suffix. `resize` uses exact
dimensions; `resize_preserving_aspect_ratio` is available as a Python API.
Rotation is counter-clockwise and expands the canvas to avoid clipping.

## Python API

For Python API imports, run from the project directory's parent and import from
`minipixel.core`, `minipixel.processing`, `minipixel.analysis`, or
`minipixel.algorithms`. Coordinate origins are top-left; image crop and region
coordinates are half-open (`left <= x < right`, `top <= y < bottom`). Pixel
comparison converts both images to RGB and requires equal dimensions.
Similarity is `1 - mean_absolute_RGB_error / 255`; it is pixelwise, not a claim
of perceptual equivalence. Hashes are grayscale average hashes encoded as
hexadecimal. Dominant color is estimated from 4-bit-per-channel RGB bins.

## Implemented functions

- **Core:** `load_image`, `save_image`, `validate_image`, `is_valid_image`,
  `get_image_dimensions`, `get_image_format`, `get_image_mode`,
  `get_image_metadata`.
- **Filters:** `convert_to_grayscale`, `adjust_brightness`, `adjust_contrast`,
  `apply_blur`, `sharpen_image`, `flip_horizontal`, `flip_vertical`,
  `rotate_image`, `invert_colors`.
- **Transformations:** `resize_image`, `resize_preserving_aspect_ratio`,
  `crop_image`, `center_crop`, `pad_image`, `thumbnail_image`.
- **Color analysis:** `calculate_average_color`, `find_dominant_color`,
  `get_color_histogram`, `count_unique_colors`, `calculate_brightness`,
  `calculate_color_distance`, `get_color_distribution`.
- **Comparison and hashes:** `compare_dimensions`,
  `calculate_mean_absolute_error`, `calculate_root_mean_square_error`,
  `calculate_image_similarity`, `generate_image_hash`,
  `are_images_identical`, `calculate_hash_distance`.
- **Pixel and geometry:** `get_pixel_value`, `set_pixel_value`,
  `calculate_region_average`, `calculate_bounding_box`, `calculate_box_area`,
  `calculate_box_intersection`, `calculate_iou`, `normalize_coordinates`.
- **Algorithm convenience API:** `calculate_similarity` (same normalized
  pixelwise score as `calculate_image_similarity`).

## Resource notes

The sample generator creates five 256x256 PNG files. Processing is single
process; NumPy-backed full-image color statistics and pixelwise comparison
allocate image-sized arrays, while Pillow handles image transforms. Exact
unique-color counting can require temporary memory proportional to image size.
To check installed package footprint in the current environment, use
`python -m pip show Pillow numpy pytest`; package size varies by platform and
Python version, so no fixed size is advertised here.
