"""Map grayscale pixels to binary characters (0/1 or space)."""

import numpy as np

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


def _calculate_grid_height(
    grid_width: int, char_aspect: float, orig_h: int, orig_w: int
) -> int:
    """Compute the number of character rows to preserve display aspect ratio.

    A monospace character is taller than wide (char_aspect ≈ width/height).
    To make the final display match the original image proportions:
        grid_height = grid_width * char_aspect * (orig_h / orig_w)
    """
    return max(1, round(grid_width * char_aspect * orig_h / orig_w))


def to_ascii(
    image: np.ndarray,
    grid_width: int = 120,
    char_aspect: float = 0.5,
    threshold: int = 128,
    invert: bool = False,
) -> list[str]:
    """Convert a grayscale image to a list of 0/1 string rows.

    Args:
        image: 2D uint8 array (grayscale), values 0-255.
        grid_width: Number of characters per row (40-400).
        char_aspect: Character width/height ratio (0.3-1.0). Monospace fonts
            are taller than wide, typically around 0.5.
        threshold: Pixel values below this become '1', others become ' '.
        invert: When True, flip '1' and ' ' (light background).

    Returns:
        List of equal-length strings; one string per row.

    Raises:
        ValueError: If any parameter is out of range or the image is not 2D.
    """
    if image.ndim != 2:
        raise ValueError(
            f"Görsel 2 boyutlu (gri ton) olmalı. Gelen şekil: {image.shape}"
        )
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

    dark_char = " " if invert else "1"
    light_char = "1" if invert else " "
    char_grid = np.where(resized < threshold, dark_char, light_char)

    return ["".join(row) for row in char_grid]