"""Floyd-Steinberg dithering for grayscale images."""

import numpy as np


def floyd_steinberg(image: np.ndarray, threshold: int = 128) -> np.ndarray:
    """Apply Floyd-Steinberg dithering to a grayscale image.

    Args:
        image: 2D uint8 grayscale array, values 0-255.
        threshold: Pivot value. Pixels above become white (255), others black (0).

    Returns:
        2D uint8 array with only 0 and 255 values.

    Raises:
        ValueError: If the image is not 2D.
    """
    if image.ndim != 2:
        raise ValueError(f"Görsel 2 boyutlu olmalı. Gelen şekil: {image.shape}")

    # Work in float so that fractional errors survive between pixels.
    pixels = image.astype(np.float32).copy()
    h, w = pixels.shape

    for y in range(h):
        for x in range(w):
            old_value = pixels[y, x]
            new_value = 255.0 if old_value >= threshold else 0.0
            pixels[y, x] = new_value

            # How far off was our decision? Push that error onto neighbors.
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

    # Errors could push values slightly below 0 or above 255; clamp them.
    return np.clip(pixels, 0, 255).astype(np.uint8)
