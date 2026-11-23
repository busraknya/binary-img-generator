"""Contrast enhancement for grayscale images."""

import numpy as np
from PIL import Image, ImageOps


def auto_contrast(image: np.ndarray) -> np.ndarray:
    """Stretch grayscale values to use the full 0-255 range.

    If the image is uniform (min == max), it is returned unchanged.
    """
    if image.ndim != 2:
        raise ValueError(f"Görsel 2 boyutlu olmalı. Gelen şekil: {image.shape}")

    min_val = int(image.min())
    max_val = int(image.max())
    if max_val == min_val:
        return image.copy()

    stretched = (image.astype(np.float32) - min_val) * (255.0 / (max_val - min_val))
    return np.clip(stretched, 0, 255).astype(np.uint8)


def equalize_histogram(image: np.ndarray) -> np.ndarray:
    """Redistribute grayscale values to improve global tonal contrast."""
    if image.ndim != 2:
        raise ValueError(f"Görsel 2 boyutlu olmalı. Gelen şekil: {image.shape}")

    pil_image = Image.fromarray(image.astype(np.uint8))
    equalized = ImageOps.equalize(pil_image)
    return np.asarray(equalized, dtype=np.uint8).copy()
