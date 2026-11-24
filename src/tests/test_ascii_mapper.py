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


def test_output_contains_only_binary_characters():
    image = np.tile(np.linspace(0, 255, 100), (100, 1)).astype(np.uint8)
    result = to_ascii(image, grid_width=40)
    assert set("".join(result)).issubset({"0", "1"})


def test_all_black_maps_to_one_binary_character():
    image = np.zeros((100, 100), dtype=np.uint8)
    result = to_ascii(image, grid_width=40, dither=False)
    assert len(set("".join(result))) == 1


def test_all_white_maps_to_one_binary_character():
    image = np.full((100, 100), 255, dtype=np.uint8)
    result = to_ascii(image, grid_width=40, dither=False)
    assert len(set("".join(result))) == 1


def test_mid_gray_uses_binary_characters():
    image = np.full((100, 100), 128, dtype=np.uint8)
    result = to_ascii(image, grid_width=40, dither=False)
    assert set("".join(result)).issubset({"0", "1"})


def test_invert_flips_binary_mapping():
    image = np.zeros((100, 100), dtype=np.uint8)
    normal = to_ascii(image, grid_width=40, invert=False, dither=False)
    inverted = to_ascii(image, grid_width=40, invert=True, dither=False)
    assert normal != inverted


@pytest.mark.parametrize(
    "pixel_value,threshold",
    [(0, 0), (255, 0), (0, 255), (255, 255)],
)
def test_threshold_keeps_binary_endpoints(pixel_value, threshold):
    image = np.full((100, 100), pixel_value, dtype=np.uint8)
    result = to_ascii(image, grid_width=40, threshold=threshold, dither=False)
    assert len(set("".join(result))) == 1


def test_threshold_moves_selected_gray_to_middle():
    image = np.full((100, 100), 100, dtype=np.uint8)
    result = to_ascii(image, grid_width=40, threshold=100, dither=False)
    assert set("".join(result)).issubset({"0", "1"})


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


def test_area_resampling_preserves_uniform_tone():
    image = np.full((120, 160), 173, dtype=np.uint8)
    result = to_ascii(image, grid_width=40, resize_method="area", dither=False)
    assert all(row == result[0] for row in result)
    assert len(result[0]) == 40


def test_nearest_resampling_remains_available():
    image = np.arange(160 * 160, dtype=np.uint8).reshape(160, 160)
    result = to_ascii(image, grid_width=40, resize_method="nearest", dither=False)
    assert len(result) == 20
    assert all(len(row) == 40 for row in result)


def test_rejects_unknown_resize_method():
    image = np.zeros((100, 100), dtype=np.uint8)
    with pytest.raises(ValueError, match="resize_method"):
        to_ascii(image, resize_method="lanczos")
