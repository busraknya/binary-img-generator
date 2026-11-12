"""Tests for image_loader."""

import numpy as np
import pytest
from PIL import Image

from binary_img_generator.image_loader import MIN_SIZE, load_image


def _make_image(tmp_path, size=(100, 100), mode="RGB", fmt="PNG"):
    """Create a test image file and return its path."""
    img = Image.new(mode, size)
    path = tmp_path / f"test.{fmt.lower()}"
    img.save(path, format=fmt)
    return path


# --- Happy path ---


def test_loads_png(tmp_path):
    path = _make_image(tmp_path, fmt="PNG")
    result = load_image(path)
    assert result.shape == (100, 100, 3)
    assert result.dtype == np.uint8


def test_loads_jpeg(tmp_path):
    path = _make_image(tmp_path, fmt="JPEG")
    result = load_image(path)
    assert result.shape == (100, 100, 3)


def test_loads_webp(tmp_path):
    path = _make_image(tmp_path, fmt="WEBP")
    result = load_image(path)
    assert result.shape == (100, 100, 3)


# --- Normalization ---


def test_converts_rgba_to_rgb(tmp_path):
    """Transparent PNGs are normalized to 3-channel RGB."""
    path = _make_image(tmp_path, mode="RGBA", fmt="PNG")
    result = load_image(path)
    assert result.shape == (100, 100, 3)


def test_converts_grayscale_to_rgb(tmp_path):
    """Grayscale PNGs are expanded to 3-channel RGB."""
    path = _make_image(tmp_path, mode="L", fmt="PNG")
    result = load_image(path)
    assert result.shape == (100, 100, 3)


# --- Size validation ---


def test_rejects_too_small(tmp_path):
    path = _make_image(tmp_path, size=(32, 32))
    with pytest.raises(ValueError, match="çok küçük"):
        load_image(path)


@pytest.mark.parametrize("size", [(MIN_SIZE - 1, MIN_SIZE), (MIN_SIZE, MIN_SIZE - 1)])
def test_rejects_just_below_min_size(tmp_path, size):
    path = _make_image(tmp_path, size=size)
    with pytest.raises(ValueError, match="çok küçük"):
        load_image(path)


def test_accepts_exactly_min_size(tmp_path):
    path = _make_image(tmp_path, size=(MIN_SIZE, MIN_SIZE))
    result = load_image(path)
    assert result.shape == (MIN_SIZE, MIN_SIZE, 3)


# --- Error paths ---


def test_rejects_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError, match="bulunamadı"):
        load_image(tmp_path / "yok.png")


def test_rejects_unsupported_format(tmp_path):
    path = _make_image(tmp_path, fmt="BMP")
    with pytest.raises(ValueError, match="Desteklenmeyen"):
        load_image(path)
