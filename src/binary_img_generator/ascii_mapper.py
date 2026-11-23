"""Map grayscale pixels to 0, 1 and space characters."""

import itertools

import numpy as np
from PIL import Image, ImageDraw

from binary_img_generator.dithering import floyd_steinberg
from binary_img_generator.png_exporter import (
    FONT_SIZE,
    _load_monospace_font,
    get_character_palette,
)

# Parameter ranges from BRD BR-05.
_MIN_GRID_WIDTH = 40
_MAX_GRID_WIDTH = 400
_MIN_CHAR_ASPECT = 0.3
_MAX_CHAR_ASPECT = 1.0
_MIN_THRESHOLD = 0
_MAX_THRESHOLD = 255
_RESIZE_METHODS = {"nearest", "area"}
_MAPPING_METHODS = {"density", "glyph"}


def _resize_nearest(image: np.ndarray, target_h: int, target_w: int) -> np.ndarray:
    """Resize a 2D array using nearest-neighbor sampling."""
    orig_h, orig_w = image.shape
    y_indices = (np.arange(target_h) * orig_h / target_h).astype(int)
    x_indices = (np.arange(target_w) * orig_w / target_w).astype(int)
    return image[y_indices[:, None], x_indices]


def _resize_area(image: np.ndarray, target_h: int, target_w: int) -> np.ndarray:
    """Resize a 2D grayscale image using area-based (box) resampling."""
    resized = Image.fromarray(image.astype(np.uint8)).resize(
        (target_w, target_h),
        resample=Image.Resampling.BOX,
    )
    return np.asarray(resized, dtype=np.uint8)


def _calculate_grid_height(grid_width: int, char_aspect: float, orig_h: int, orig_w: int) -> int:
    """Compute row count so display aspect ratio matches the source image."""
    height = round(grid_width * char_aspect * orig_h / orig_w)
    return max(1, height)


def _adjust_midpoint(image: np.ndarray, threshold: int) -> np.ndarray:
    """Move the selected grayscale value to the middle while preserving endpoints."""
    if threshold in (0, 128, 255):
        return image.copy()

    values = image.astype(np.float32)
    adjusted = np.empty_like(values)
    lower = values <= threshold
    adjusted[lower] = values[lower] * (128.0 / threshold)
    adjusted[~lower] = 128.0 + (values[~lower] - threshold) * (127.0 / (255 - threshold))
    return np.clip(np.rint(adjusted), 0, 255).astype(np.uint8)


def _to_ascii_glyph(
    image: np.ndarray,
    grid_width: int,
    grid_height: int,
    invert: bool,
) -> list[str]:
    """Choose the rendered glyph that best matches each source image cell."""
    font = _load_monospace_font(FONT_SIZE)
    char_width = max(1, int(np.ceil(font.getlength("M"))))
    char_height = int(FONT_SIZE * 1.2)

    target = Image.fromarray(image.astype(np.uint8)).resize(
        (grid_width * char_width, grid_height * char_height),
        resample=Image.Resampling.BOX,
    )
    target_array = np.asarray(target, dtype=np.float32)
    if invert:
        target_array = 255.0 - target_array

    characters = (" ", "1", "0")
    masks = []
    for character in characters:
        cell = Image.new("L", (char_width, char_height), 0)
        ImageDraw.Draw(cell).text((0, 0), character, fill=255, font=font)
        masks.append(np.asarray(cell, dtype=np.float32))

    mask_array = np.stack(masks)
    output = np.empty((grid_height, grid_width), dtype="<U1")

    for row in range(grid_height):
        y_start = row * char_height
        for col in range(grid_width):
            x_start = col * char_width
            patch = target_array[
                y_start : y_start + char_height,
                x_start : x_start + char_width,
            ]
            errors = np.mean((mask_array - patch[None, :, :]) ** 2, axis=(1, 2))
            output[row, col] = characters[int(np.argmin(errors))]

    return ["".join(row) for row in output]


def to_ascii(
    image: np.ndarray,
    grid_width: int = 120,
    char_aspect: float = 0.5,
    threshold: int = 128,
    invert: bool = False,
    dither: bool = True,
    resize_method: str = "nearest",
    mapping_method: str = "density",
) -> list[str]:
    """Convert a grayscale image to rows of 0, 1 and space characters.

    Args:
        image: 2D uint8 array (grayscale), values 0-255.
        grid_width: Number of characters per row (40-400).
        char_aspect: Character width/height ratio (0.3-1.0).
        threshold: Grayscale value mapped to the middle tone (default 128).
        invert: Reverse the character-density mapping.
        dither: Apply Floyd-Steinberg dithering (default True).
        resize_method: "nearest" for point sampling or "area" for box resampling.
        mapping_method: "density" for tone mapping or "glyph" for rendered-shape matching.

    Returns:
        List of equal-length strings; one string per row.

    Raises:
        ValueError: If any parameter is out of range or the image is not 2D.
    """
    if image.ndim != 2:
        raise ValueError(f"Görsel 2 boyutlu (gri ton) olmalı. Gelen şekil: {image.shape}")
    if not (_MIN_GRID_WIDTH <= grid_width <= _MAX_GRID_WIDTH):
        raise ValueError(
            f"grid_width {_MIN_GRID_WIDTH}-{_MAX_GRID_WIDTH} aralığında olmalı. "
            f"Gelen: {grid_width}"
        )
    if not (_MIN_CHAR_ASPECT <= char_aspect <= _MAX_CHAR_ASPECT):
        raise ValueError(
            f"char_aspect {_MIN_CHAR_ASPECT}-{_MAX_CHAR_ASPECT} aralığında olmalı. "
            f"Gelen: {char_aspect}"
        )
    if not (_MIN_THRESHOLD <= threshold <= _MAX_THRESHOLD):
        raise ValueError(
            f"threshold {_MIN_THRESHOLD}-{_MAX_THRESHOLD} aralığında olmalı. " f"Gelen: {threshold}"
        )
    if mapping_method not in _MAPPING_METHODS:
        raise ValueError("mapping_method must be density or glyph")
    if resize_method not in _RESIZE_METHODS:
        raise ValueError(
            f"resize_method şu değerlerden biri olmalı: {', '.join(sorted(_RESIZE_METHODS))}"
        )

    orig_h, orig_w = image.shape
    grid_height = _calculate_grid_height(grid_width, char_aspect, orig_h, orig_w)
    if mapping_method == "glyph":
        # Keep the original image detail until it is resized to the final
        # rendered character-grid dimensions inside the glyph matcher.
        return _to_ascii_glyph(image, grid_width, grid_height, invert)

    if resize_method == "area":
        resized = _resize_area(image, grid_height, grid_width)
    else:
        resized = _resize_nearest(image, grid_height, grid_width)

    resized = _adjust_midpoint(resized, threshold)

    palette = get_character_palette()
    characters = [character for character, _ in palette]
    levels = tuple(level for _, level in palette)

    if dither:
        quantized = floyd_steinberg(resized, levels=levels)
    else:
        boundaries = [(left + right) / 2 for left, right in itertools.pairwise(levels)]
        indices = np.digitize(resized, boundaries)
        quantized = np.asarray(levels, dtype=np.uint8)[indices]

    if invert:
        characters.reverse()

    character_by_level = dict(zip(levels, characters))
    char_grid = np.empty(quantized.shape, dtype="<U1")
    for level, character in character_by_level.items():
        char_grid[quantized == level] = character

    return ["".join(row) for row in char_grid]
