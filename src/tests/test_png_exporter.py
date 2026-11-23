"""Tests for png_exporter."""

import numpy as np
import pytest
from PIL import Image

from binary_img_generator.png_exporter import export_png, get_character_palette


def test_creates_png_file(tmp_path):
    output = tmp_path / "test.png"
    export_png(["10 ", " 01", "110"], output)
    assert output.exists()
    assert output.suffix == ".png"


def test_creates_parent_dirs(tmp_path):
    output = tmp_path / "nested" / "deep" / "test.png"
    export_png(["0"], output)
    assert output.exists()


def test_all_spaces_produces_black_image(tmp_path):
    output = tmp_path / "test.png"
    export_png(["   ", "   "], output)
    pixels = np.array(Image.open(output).convert("RGB"))
    assert pixels.min() == 0 and pixels.max() == 0


def test_palette_has_three_characters_in_density_order():
    palette = get_character_palette()
    assert {character for character, _ in palette} == {" ", "0", "1"}
    levels = [level for _, level in palette]
    assert levels == sorted(set(levels))
    assert levels[0] == 0
    assert levels[-1] == 255


def test_rejects_empty_list(tmp_path):
    with pytest.raises(ValueError, match="boş"):
        export_png([], tmp_path / "test.png")


def test_rejects_ragged_rows(tmp_path):
    with pytest.raises(ValueError, match="Satır"):
        export_png(["10", "1"], tmp_path / "test.png")


def test_rejects_unsupported_characters(tmp_path):
    with pytest.raises(ValueError, match="Desteklenmeyen"):
        export_png(["1x0"], tmp_path / "test.png")


def test_output_width_scales_with_grid(tmp_path):
    small = tmp_path / "small.png"
    large = tmp_path / "large.png"
    export_png(["1" * 8], small)
    export_png(["1" * 40], large)
    assert Image.open(large).size[0] > Image.open(small).size[0]
