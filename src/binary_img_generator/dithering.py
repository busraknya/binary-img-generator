"""Floyd-Steinberg dithering for grayscale images."""

import numpy as np


def floyd_steinberg(
    image: np.ndarray,
    threshold: int = 128,
    levels: tuple[int, ...] | list[int] | None = None,
) -> np.ndarray:
    """Apply Floyd-Steinberg error diffusion to a grayscale image.

    Args:
        image: 2D uint8 grayscale array, values 0-255.
        threshold: Black/white pivot used by the default two-level mode.
        levels: Optional ordered output levels. When provided, each pixel is
            mapped to its nearest level. For example, (0, 166, 255).

    Returns:
        2D uint8 array containing only the selected output levels.

    Raises:
        ValueError: If the image is not 2D or levels are invalid.
    """
    if image.ndim != 2:
        raise ValueError(f"Görsel 2 boyutlu olmalı. Gelen şekil: {image.shape}")

    if levels is not None:
        if len(levels) < 2:
            raise ValueError("En az iki dithering seviyesi gerekli.")
        if any(level < 0 or level > 255 for level in levels):
            raise ValueError("Dithering seviyeleri 0-255 aralığında olmalı.")
        if list(levels) != sorted(set(levels)):
            raise ValueError("Dithering seviyeleri benzersiz ve artan sırada olmalı.")
        output_levels = np.asarray(levels, dtype=np.float32)
    else:
        output_levels = np.asarray([0.0, 255.0], dtype=np.float32)

    pixels = image.astype(np.float32).copy()
    h, w = pixels.shape

    for y in range(h):
        for x in range(w):
            old_value = pixels[y, x]

            if levels is None:
                new_value = 255.0 if old_value >= threshold else 0.0
            else:
                new_value = output_levels[np.argmin(np.abs(output_levels - old_value))]

            pixels[y, x] = new_value
            error = old_value - new_value

            # Floyd-Steinberg distribution:
            #       current   (7/16)
            #   (3/16)  (5/16)  (1/16)
            if x + 1 < w:
                pixels[y, x + 1] += error * 7 / 16
            if y + 1 < h:
                if x > 0:
                    pixels[y + 1, x - 1] += error * 3 / 16
                pixels[y + 1, x] += error * 5 / 16
                if x + 1 < w:
                    pixels[y + 1, x + 1] += error * 1 / 16

    return np.clip(pixels, 0, 255).astype(np.uint8)
