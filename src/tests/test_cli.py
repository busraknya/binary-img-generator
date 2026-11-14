"""Tests for the CLI."""

import pytest
from PIL import Image

from binary_img_generator.cli import main


def _make_test_image(tmp_path, size=(100, 100)):
    path = tmp_path / "test.png"
    Image.new("RGB", size, "gray").save(path)
    return path


def test_happy_path(tmp_path):
    img_path = _make_test_image(tmp_path)
    out_path = tmp_path / "out.png"
    code = main([str(img_path), "--output", str(out_path), "--grid-width", "40"])
    assert code == 0
    assert out_path.exists()


def test_default_output_when_omitted(tmp_path, monkeypatch):
    # Change cwd so the default output/ dir is written under tmp_path
    monkeypatch.chdir(tmp_path)
    img_path = _make_test_image(tmp_path)
    code = main([str(img_path), "--grid-width", "40"])
    assert code == 0
    # Look for any portre_*.png under output/
    outputs = list((tmp_path / "output").glob("portre_*.png"))
    assert len(outputs) == 1


def test_missing_file_returns_error_code(tmp_path, capsys):
    code = main([str(tmp_path / "yok.png")])
    assert code == 1
    captured = capsys.readouterr()
    assert "bulunamadı" in captured.err


def test_invalid_grid_width_returns_error_code(tmp_path, capsys):
    img_path = _make_test_image(tmp_path)
    code = main([str(img_path), "--grid-width", "10"])
    assert code == 1
    captured = capsys.readouterr()
    assert "grid_width" in captured.err


def test_invert_flag(tmp_path):
    img_path = _make_test_image(tmp_path)
    out_path = tmp_path / "out.png"
    code = main([str(img_path), "--output", str(out_path), "--grid-width", "40", "--invert"])
    assert code == 0
    assert out_path.exists()
