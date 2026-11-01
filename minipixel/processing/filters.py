"""Common point and neighborhood image filters."""

from numbers import Real

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

from ..utils.validators import require_image, require_nonnegative_real


def convert_to_grayscale(image: Image.Image) -> Image.Image:
    """Return an 8-bit grayscale (``L``) copy."""
    require_image(image)
    return ImageOps.grayscale(image)


def adjust_brightness(image: Image.Image, factor: Real) -> Image.Image:
    """Scale brightness; 0 is black, 1 preserves input, values above 1 brighten."""
    require_image(image)
    if isinstance(factor, bool) or not isinstance(factor, Real):
        raise TypeError("factor must be a real number")
    require_nonnegative_real(factor, "factor")
    return ImageEnhance.Brightness(image).enhance(float(factor))


def adjust_contrast(image: Image.Image, factor: Real) -> Image.Image:
    """Scale contrast; 0 is neutral gray, 1 preserves input."""
    require_image(image)
    if isinstance(factor, bool) or not isinstance(factor, Real):
        raise TypeError("factor must be a real number")
    require_nonnegative_real(factor, "factor")
    return ImageEnhance.Contrast(image).enhance(float(factor))


def apply_blur(image: Image.Image, radius: Real) -> Image.Image:
    """Return a Gaussian-blurred copy with a finite, non-negative radius."""
    require_image(image)
    require_nonnegative_real(radius, "radius")
    return image.filter(ImageFilter.GaussianBlur(float(radius)))


def sharpen_image(image: Image.Image) -> Image.Image:
    """Return a sharpened copy using Pillow's built-in sharpening filter."""
    require_image(image)
    return image.filter(ImageFilter.SHARPEN)


def flip_horizontal(image: Image.Image) -> Image.Image:
    """Mirror an image left-to-right."""
    require_image(image)
    return ImageOps.mirror(image)


def flip_vertical(image: Image.Image) -> Image.Image:
    """Mirror an image top-to-bottom."""
    require_image(image)
    return ImageOps.flip(image)


def rotate_image(image: Image.Image, angle: Real) -> Image.Image:
    """Rotate counter-clockwise by degrees, expanding to avoid clipping."""
    require_image(image)
    if isinstance(angle, bool) or not isinstance(angle, Real):
        raise TypeError("angle must be a real number")
    if not float(angle) == float(angle) or float(angle) in (float("inf"), float("-inf")):
        raise ValueError("angle must be finite")
    return image.rotate(float(angle), expand=True)


def invert_colors(image: Image.Image) -> Image.Image:
    """Invert color channels while preserving alpha for RGB/RGBA images."""
    require_image(image)
    if image.mode == "RGBA":
        red, green, blue, alpha = image.split()
        inverted = ImageOps.invert(Image.merge("RGB", (red, green, blue)))
        inverted.putalpha(alpha)
        return inverted
    if image.mode == "LA":
        luminance, alpha = image.split()
        result = ImageOps.invert(luminance)
        result.putalpha(alpha)
        return result
    if image.mode == "P":
        return ImageOps.invert(image.convert("RGB"))
    if image.mode == "1":
        return ImageOps.invert(image.convert("L"))
    if image.mode in ("L", "RGB"):
        return ImageOps.invert(image)
    return ImageOps.invert(image.convert("RGB"))
