"""Tests for Floyd-Steinberg dithering."""

import numpy as np
import pytest

from binary_img_generator.dithering import floyd_steinberg


def test_output_is_only_black_or_white():
    gradient = np.tile(np.linspace(0, 255, 20), (20, 1)).astype(np.uint8)
    result = floyd_steinberg(gradient)
    unique_values = set(np.unique(result).tolist())
    assert unique_values.issubset({0, 255})


def test_all_black_stays_black():
    image = np.zeros((10, 10), dtype=np.uint8)
    result = floyd_steinberg(image)
    assert np.all(result == 0)


def test_all_white_stays_white():
    image = np.full((10, 10), 255, dtype=np.uint8)
    result = floyd_steinberg(image)
    assert np.all(result == 255)


def test_50_percent_gray_produces_mix():
    """A gray image should produce roughly half black, half white pixels."""
    image = np.full((20, 20), 128, dtype=np.uint8)
    result = floyd_steinberg(image, threshold=128)
    white_ratio = (result == 255).sum() / result.size
    assert 0.4 < white_ratio < 0.6


def test_rejects_non_2d():
    with pytest.raises(ValueError, match="2 boyutlu"):
        floyd_steinberg(np.zeros((10, 10, 3), dtype=np.uint8))
