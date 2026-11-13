"""Tests for png_exporter."""

import numpy as np
import pytest
from PIL import Image

from binary_img_generator.png_exporter import export_png


def test_creates_png_file(tmp_path):
    output = tmp_path / "test.png"
    export_png(["111", "   ", "111"], output)
    assert output.exists()
    assert output.suffix == ".png"


def test_creates_parent_dirs(tmp_path):
    output = tmp_path / "nested" / "deep" / "test.png"
    export_png(["1"], output)
    assert output.exists()


def test_all_spaces_produces_black_image(tmp_path):
    output = tmp_path / "test.png"
    export_png(["   ", "   "], output)
    img = Image.open(output).convert("RGB")
    pixels = np.array(img)
    assert pixels.min() == 0 and pixels.max() == 0


def test_rejects_empty_list(tmp_path):
    with pytest.raises(ValueError, match="boş"):
        export_png([], tmp_path / "test.png")


def test_rejects_ragged_rows(tmp_path):
    with pytest.raises(ValueError, match="Satır"):
        export_png(["11", "1"], tmp_path / "test.png")


def test_output_width_scales_with_grid(tmp_path):
    small = tmp_path / "small.png"
    large = tmp_path / "large.png"
    export_png(["1" * 8], small)
    export_png(["1" * 40], large)
    assert Image.open(large).size[0] > Image.open(small).size[0]
