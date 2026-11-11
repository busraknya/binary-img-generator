"""Grayscale conversion using ITU-R BT.601 weights."""

import numpy as np

# ITU-R BT.601 luma coefficients.
# Human eyes are more sensitive to green, less to blue.
_BT601_R = 0.299
_BT601_G = 0.587
_BT601_B = 0.114


def to_grayscale(image: np.ndarray) -> np.ndarray:
    """Convert an RGB image to grayscale using BT.601 weights.

    Args:
        image: Array of shape (height, width, 3) with dtype uint8.

    Returns:
        Array of shape (height, width) with dtype uint8, values 0-255.

    Raises:
        ValueError: If the input is not a 3-channel uint8 image.
    """
    if image.ndim != 3 or image.shape[2] != 3:
        raise ValueError(
            f"Görsel 3 kanallı (RGB) olmalı. Gelen şekil: {image.shape}"
        )
    if image.dtype != np.uint8:
        raise ValueError(
            f"Görsel verisi uint8 olmalı. Gelen tip: {image.dtype}"
        )

    # Compute in float32 to avoid integer overflow, then round to nearest.
    weighted = (
        _BT601_R * image[:, :, 0].astype(np.float32)
        + _BT601_G * image[:, :, 1].astype(np.float32)
        + _BT601_B * image[:, :, 2].astype(np.float32)
    )
    return np.round(weighted).astype(np.uint8)