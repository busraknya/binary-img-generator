"""Load image files from disk as RGB numpy arrays."""

from pathlib import Path

import numpy as np
from PIL import Image

# Images smaller than this are rejected: no face detail to work with (BR-01).
MIN_SIZE = 64

# Pillow reports the real file format (by content, not extension).
SUPPORTED_FORMATS = {"JPEG", "PNG", "WEBP"}


def load_image(path: str | Path) -> np.ndarray:
    """Load an image file and return it as an RGB numpy array.

    Args:
        path: Path to the image file (JPEG, PNG, or WebP).

    Returns:
        Array of shape (height, width, 3) with dtype uint8.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the format is unsupported or the image is too small.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Dosya bulunamadı: {path}")

    with Image.open(path) as img:
        if img.format not in SUPPORTED_FORMATS:
            supported = ", ".join(sorted(SUPPORTED_FORMATS))
            raise ValueError(
                f"Desteklenmeyen format: {img.format}. " f"Desteklenenler: {supported}"
            )

        width, height = img.size
        if width < MIN_SIZE or height < MIN_SIZE:
            raise ValueError(
                f"Görsel çok küçük ({width}×{height}). "
                f"En az {MIN_SIZE}×{MIN_SIZE} piksel olmalı."
            )

        # Normalize to 3-channel RGB (handles RGBA, grayscale, palette).
        rgb = img.convert("RGB")
        return np.array(rgb, dtype=np.uint8)
