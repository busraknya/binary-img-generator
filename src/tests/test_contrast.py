"""Tests for auto-contrast."""

import numpy as np
import pytest

from binary_img_generator.contrast import auto_contrast


def test_stretches_narrow_range():
    image = np.array([[100, 150], [120, 170]], dtype=np.uint8)
    result = auto_contrast(image)
    assert result.min() == 0
    assert result.max() == 255


def test_uniform_image_unchanged():
    image = np.full((10, 10), 128, dtype=np.uint8)
    result = auto_contrast(image)
    assert np.all(result == 128)


def test_already_full_range_unchanged():
    image = np.array([[0, 255], [128, 64]], dtype=np.uint8)
    result = auto_contrast(image)
    assert result.min() == 0
    assert result.max() == 255


def test_rejects_non_2d():
    with pytest.raises(ValueError, match="2 boyutlu"):
        auto_contrast(np.zeros((10, 10, 3), dtype=np.uint8))
