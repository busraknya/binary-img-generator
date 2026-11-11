"""Tests for ascii_mapper."""

import numpy as np
import pytest

from binary_img_generator.ascii_mapper import to_ascii


def test_output_is_list_of_strings():
    image = np.full((100, 100), 128, dtype=np.uint8)
    result = to_ascii(image, grid_width=40)
    assert isinstance(result, list)
    assert all(isinstance(row, str) for row in result)


def test_all_rows_same_length():
    image = np.full((100, 100), 128, dtype=np.uint8)
    result = to_ascii(image, grid_width=80)
    lengths = {len(row) for row in result}
    assert lengths == {80}


def test_all_black_produces_all_ones():
    image = np.zeros((100, 100), dtype=np.uint8)
    result = to_ascii(image, grid_width=40)
    assert all(row == "1" * 40 for row in result)


def test_all_white_produces_all_spaces():
    image = np.full((100, 100), 255, dtype=np.uint8)
    result = to_ascii(image, grid_width=40)
    assert all(row == " " * 40 for row in result)


def test_invert_flips_dark_and_light():
    black = np.zeros((100, 100), dtype=np.uint8)
    inverted = to_ascii(black, grid_width=40, invert=True)
    assert all(row == " " * 40 for row in inverted)


@pytest.mark.parametrize(
    "pixel_value,threshold,expected_char",
    [
        (100, 101, "1"),  # 100 < 101 → dark
        (100, 100, " "),  # 100 < 100 is False → light
        (100, 99, " "),   # 100 < 99 is False → light
        (0, 1, "1"),      # 0 < 1 → dark
        (255, 255, " "),  # 255 < 255 is False → light
    ],
)
def test_threshold_boundaries(pixel_value, threshold, expected_char):
    image = np.full((100, 100), pixel_value, dtype=np.uint8)
    result = to_ascii(image, grid_width=40, threshold=threshold)
    assert all(row == expected_char * 40 for row in result)


def test_grid_height_preserves_aspect_square():
    """Square input with char_aspect=0.5 → half the rows (100×0.5 = 50)."""
    image = np.full((100, 100), 128, dtype=np.uint8)
    result = to_ascii(image, grid_width=100, char_aspect=0.5)
    assert len(result) == 50


def test_grid_height_preserves_aspect_wide():
    """2:1 wide input → quarter rows (100 × 0.5 × 50/100 = 25)."""
    image = np.full((50, 100), 128, dtype=np.uint8)
    result = to_ascii(image, grid_width=100, char_aspect=0.5)
    assert len(result) == 25


def test_grid_height_minimum_one():
    """Very wide inputs should still produce at least 1 row."""
    image = np.full((1, 1000), 128, dtype=np.uint8)
    result = to_ascii(image, grid_width=40, char_aspect=0.3)
    assert len(result) >= 1


def test_rejects_3d_image():
    with pytest.raises(ValueError, match="2 boyutlu"):
        to_ascii(np.zeros((10, 10, 3), dtype=np.uint8))


@pytest.mark.parametrize("bad_width", [10, 39, 401, 500])
def test_rejects_out_of_range_grid_width(bad_width):
    image = np.zeros((100, 100), dtype=np.uint8)
    with pytest.raises(ValueError, match="grid_width"):
        to_ascii(image, grid_width=bad_width)


@pytest.mark.parametrize("bad_aspect", [0.1, 0.29, 1.1, 2.0])
def test_rejects_out_of_range_char_aspect(bad_aspect):
    image = np.zeros((100, 100), dtype=np.uint8)
    with pytest.raises(ValueError, match="char_aspect"):
        to_ascii(image, char_aspect=bad_aspect)


@pytest.mark.parametrize("bad_threshold", [-1, 256, 1000])
def test_rejects_out_of_range_threshold(bad_threshold):
    image = np.zeros((100, 100), dtype=np.uint8)
    with pytest.raises(ValueError, match="threshold"):
        to_ascii(image, threshold=bad_threshold)