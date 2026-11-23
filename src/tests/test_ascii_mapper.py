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
    assert {len(row) for row in result} == {80}


def test_all_black_produces_spaces():
    image = np.zeros((100, 100), dtype=np.uint8)
    result = to_ascii(image, grid_width=40, dither=False)
    assert all(row == " " * 40 for row in result)


def test_all_white_produces_zeros():
    image = np.full((100, 100), 255, dtype=np.uint8)
    result = to_ascii(image, grid_width=40, dither=False)
    assert all(row == "0" * 40 for row in result)


def test_mid_gray_uses_middle_density_character():
    image = np.full((100, 100), 128, dtype=np.uint8)
    result = to_ascii(image, grid_width=40, dither=False)
    assert all(row == "1" * 40 for row in result)


def test_invert_flips_dark_and_light():
    black = np.zeros((100, 100), dtype=np.uint8)
    inverted = to_ascii(black, grid_width=40, invert=True, dither=False)
    assert all(row == "0" * 40 for row in inverted)


@pytest.mark.parametrize(
    "pixel_value,threshold,expected_char",
    [
        (0, 0, " "),
        (255, 0, "0"),
        (0, 255, " "),
        (255, 255, "0"),
    ],
)
def test_threshold_endpoints_preserve_black_and_white(pixel_value, threshold, expected_char):
    image = np.full((100, 100), pixel_value, dtype=np.uint8)
    result = to_ascii(image, grid_width=40, threshold=threshold, dither=False)
    assert all(row == expected_char * 40 for row in result)


def test_threshold_moves_selected_gray_to_middle():
    image = np.full((100, 100), 100, dtype=np.uint8)
    result = to_ascii(image, grid_width=40, threshold=100, dither=False)
    assert all(row == "1" * 40 for row in result)


def test_threshold_changes_relative_tone_mapping():
    image = np.full((100, 100), 80, dtype=np.uint8)
    darker_midpoint = to_ascii(image, grid_width=40, threshold=160, dither=False)
    lighter_midpoint = to_ascii(image, grid_width=40, threshold=100, dither=False)
    assert all(row == " " * 40 for row in darker_midpoint)
    assert all(row == "1" * 40 for row in lighter_midpoint)


def test_grid_height_preserves_aspect_square():
    image = np.full((100, 100), 128, dtype=np.uint8)
    result = to_ascii(image, grid_width=100, char_aspect=0.5)
    assert len(result) == 50


def test_grid_height_preserves_aspect_wide():
    image = np.full((50, 100), 128, dtype=np.uint8)
    result = to_ascii(image, grid_width=100, char_aspect=0.5)
    assert len(result) == 25


def test_grid_height_minimum_one():
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
