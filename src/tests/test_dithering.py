"""Tests for Floyd-Steinberg dithering."""

import numpy as np
import pytest

from binary_img_generator.dithering import floyd_steinberg


def test_output_is_only_black_or_white():
    gradient = np.tile(np.linspace(0, 255, 20), (20, 1)).astype(np.uint8)
    result = floyd_steinberg(gradient)
    assert set(np.unique(result).tolist()).issubset({0, 255})


def test_all_black_stays_black():
    image = np.zeros((10, 10), dtype=np.uint8)
    result = floyd_steinberg(image)
    assert np.all(result == 0)


def test_all_white_stays_white():
    image = np.full((10, 10), 255, dtype=np.uint8)
    result = floyd_steinberg(image)
    assert np.all(result == 255)


def test_50_percent_gray_produces_mix():
    image = np.full((20, 20), 128, dtype=np.uint8)
    result = floyd_steinberg(image, threshold=128)
    white_ratio = (result == 255).sum() / result.size
    assert 0.4 < white_ratio < 0.6


def test_three_level_dithering_uses_only_given_levels():
    image = np.tile(np.linspace(0, 255, 30), (30, 1)).astype(np.uint8)
    levels = (0, 166, 255)
    result = floyd_steinberg(image, levels=levels)
    assert set(np.unique(result).tolist()).issubset(set(levels))
    assert set(np.unique(result).tolist()) == set(levels)


def test_three_level_dithering_preserves_average_tone():
    image = np.full((100, 100), 128, dtype=np.uint8)
    result = floyd_steinberg(image, levels=(0, 166, 255))
    assert abs(float(result.mean()) - 128) < 3


@pytest.mark.parametrize("levels", [(), (128,), (0, 128, 128), (255, 0), (-1, 255), (0, 256)])
def test_rejects_invalid_levels(levels):
    image = np.zeros((10, 10), dtype=np.uint8)
    with pytest.raises(ValueError):
        floyd_steinberg(image, levels=levels)


def test_rejects_non_2d():
    with pytest.raises(ValueError, match="2 boyutlu"):
        floyd_steinberg(np.zeros((10, 10, 3), dtype=np.uint8))
