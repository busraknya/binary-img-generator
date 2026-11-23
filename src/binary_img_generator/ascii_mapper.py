"""Map grayscale pixels to 0, 1 and space characters."""

import numpy as np

from binary_img_generator.dithering import floyd_steinberg
from binary_img_generator.png_exporter import get_character_palette

# Parameter ranges from BRD BR-05.
_MIN_GRID_WIDTH = 40
_MAX_GRID_WIDTH = 400
_MIN_CHAR_ASPECT = 0.3
_MAX_CHAR_ASPECT = 1.0
_MIN_THRESHOLD = 0
_MAX_THRESHOLD = 255


def _resize_nearest(image: np.ndarray, target_h: int, target_w: int) -> np.ndarray:
    """Resize a 2D array using nearest-neighbor sampling."""
    orig_h, orig_w = image.shape
    y_indices = (np.arange(target_h) * orig_h / target_h).astype(int)
    x_indices = (np.arange(target_w) * orig_w / target_w).astype(int)
    return image[y_indices[:, None], x_indices]


def _calculate_grid_height(grid_width: int, char_aspect: float, orig_h: int, orig_w: int) -> int:
    """Compute row count so display aspect ratio matches the source image."""
    height = round(grid_width * char_aspect * orig_h / orig_w)
    return max(1, height)


def _adjust_midpoint(image: np.ndarray, threshold: int) -> np.ndarray:
    """Move the selected grayscale value to the middle of the tone range."""
    if threshold == 128:
        return image.copy()

    values = image.astype(np.float32)
    adjusted = np.empty_like(values)

    if threshold == 0:
        adjusted = 128.0 + values * (127.0 / 255.0)
    elif threshold == 255:
        adjusted = values * (128.0 / 255.0)
    else:
        lower = values <= threshold
        adjusted[lower] = values[lower] * (128.0 / threshold)
        adjusted[~lower] = 128.0 + (values[~lower] - threshold) * (
            127.0 / (255 - threshold)
        )

    return np.clip(np.rint(adjusted), 0, 255).astype(np.uint8)


def to_ascii(
    image: np.ndarray,
    grid_width: int = 120,
    char_aspect: float = 0.5,
    threshold: int = 128,
    invert: bool = False,
    dither: bool = True,
) -> list[str]:
    """Convert a grayscale image to rows of 0, 1 and space characters.

    Args:
        image: 2D uint8 array (grayscale), values 0-255.
        grid_width: Number of characters per row (40-400).
        char_aspect: Character width/height ratio (0.3-1.0).
        threshold: Grayscale value mapped to the middle of the tone range.
        invert: Reverse the character-density mapping.
        dither: Apply Floyd-Steinberg dithering (default True).

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
            f"threshold {_MIN_THRESHOLD}-{_MAX_THRESHOLD} aralığında olmalı. "
            f"Gelen: {threshold}"
        )

    orig_h, orig_w = image.shape
    grid_height = _calculate_grid_height(grid_width, char_aspect, orig_h, orig_w)
    resized = _resize_nearest(image, grid_height, grid_width)
    resized = _adjust_midpoint(resized, threshold)

    palette = get_character_palette()
    characters = [character for character, _ in palette]
    levels = tuple(level for _, level in palette)

    if dither:
        quantized = floyd_steinberg(resized, levels=levels)
    else:
        boundaries = [(left + right) / 2 for left, right in zip(levels, levels[1:])]
        indices = np.digitize(resized, boundaries)
        quantized = np.asarray(levels, dtype=np.uint8)[indices]

    if invert:
        characters.reverse()

    character_by_level = dict(zip(levels, characters))
    char_grid = np.empty(quantized.shape, dtype="<U1")
    for level, character in character_by_level.items():
        char_grid[quantized == level] = character

    return ["".join(row) for row in char_grid]
