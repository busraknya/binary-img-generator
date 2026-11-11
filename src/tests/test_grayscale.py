"""Tests for grayscale conversion."""

import numpy as np
import pytest

from binary_img_generator.grayscale import to_grayscale


@pytest.mark.parametrize(
    "rgb,expected",
    [
        ((255, 0, 0), 76),  # pure red   → 0.299 × 255 ≈ 76.2
        ((0, 255, 0), 150),  # pure green → 0.587 × 255 ≈ 149.7
        ((0, 0, 255), 29),  # pure blue  → 0.114 × 255 ≈ 29.1
        ((255, 255, 255), 255),  # white
        ((0, 0, 0), 0),  # black
        ((128, 128, 128), 128),  # mid-gray stays mid-gray
    ],
)
def test_bt601_weights(rgb, expected):
    """BT.601 weights must be applied within ±1 tolerance."""
    pixel = np.array([[rgb]], dtype=np.uint8)
    result = to_grayscale(pixel)
    assert abs(int(result[0, 0]) - expected) <= 1


def test_output_shape_and_dtype():
    """Output must be 2D and uint8 regardless of input size."""
    image = np.zeros((10, 20, 3), dtype=np.uint8)
    result = to_grayscale(image)
    assert result.shape == (10, 20)
    assert result.dtype == np.uint8


def test_rejects_non_rgb():
    """A 2D array (grayscale) should be rejected with a clear error."""
    with pytest.raises(ValueError, match="3 kanallı"):
        to_grayscale(np.zeros((10, 10), dtype=np.uint8))


def test_rejects_wrong_dtype():
    """Float arrays are not accepted; input must be uint8."""
    with pytest.raises(ValueError, match="uint8"):
        to_grayscale(np.zeros((10, 10, 3), dtype=np.float32))
