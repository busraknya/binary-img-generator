"""Tests for contrast enhancement methods."""

import numpy as np
import pytest

from binary_img_generator.contrast import (
    auto_contrast,
    equalize_histogram,
    percentile_contrast,
)


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


def test_equalize_histogram_returns_uint8_and_same_shape():
    image = np.tile(np.arange(16, dtype=np.uint8), (16, 1))
    result = equalize_histogram(image)
    assert result.shape == image.shape
    assert result.dtype == np.uint8


def test_equalize_histogram_handles_uniform_image():
    image = np.full((10, 10), 128, dtype=np.uint8)
    result = equalize_histogram(image)
    assert result.shape == image.shape
    assert result.dtype == np.uint8


def test_equalize_histogram_rejects_non_2d():
    with pytest.raises(ValueError, match="2 boyutlu"):
        equalize_histogram(np.zeros((10, 10, 3), dtype=np.uint8))


def test_percentile_contrast_stretches_values():
    image = np.tile(np.arange(10, dtype=np.uint8), (10, 1)) + 100
    result = percentile_contrast(image, 0, 100)
    assert result.min() == 0
    assert result.max() == 255


def test_percentile_contrast_clips_outliers():
    image = np.full((10, 10), 100, dtype=np.uint8)
    image[0, 0] = 0
    image[-1, -1] = 255
    result = percentile_contrast(image)
    assert result.shape == image.shape
    assert result.dtype == np.uint8


def test_percentile_contrast_handles_uniform_image():
    image = np.full((10, 10), 128, dtype=np.uint8)
    result = percentile_contrast(image)
    assert np.array_equal(result, image)


def test_percentile_contrast_rejects_invalid_percentiles():
    image = np.arange(100, dtype=np.uint8).reshape(10, 10)
    with pytest.raises(ValueError, match="Yüzdelik"):
        percentile_contrast(image, 99, 1)


def test_percentile_contrast_rejects_non_2d():
    with pytest.raises(ValueError, match="2 boyutlu"):
        percentile_contrast(np.zeros((10, 10, 3), dtype=np.uint8))
