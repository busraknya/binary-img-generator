"""Export binary character art as a PNG."""

from math import ceil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Font size in pixels. At 28px with monospace, 120 chars produce a large PNG.
FONT_SIZE = 28

# Common monospace font paths. First one that loads wins.
_FONT_CANDIDATES = [
    "/System/Library/Fonts/Menlo.ttc",  # macOS
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",  # Linux
    "C:\\Windows\\Fonts\\consola.ttf",  # Windows
]


def _load_monospace_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Load a monospace font, falling back to Pillow's default."""
    for font_path in _FONT_CANDIDATES:
        if Path(font_path).exists():
            try:
                return ImageFont.truetype(font_path, size)
            except OSError:
                continue
    return ImageFont.load_default(size=size)


def get_character_palette() -> tuple[tuple[str, int], ...]:
    """Return 1 and 0 ordered by their measured visual density.

    Density is measured with the same font and cell size used by the PNG
    exporter. The returned numeric levels are normalized to the densest glyph.
    """
    font = _load_monospace_font(FONT_SIZE)
    char_width = max(1, ceil(font.getlength("M")))
    char_height = int(FONT_SIZE * 1.2)
    cell_area = char_width * char_height

    measured: list[tuple[str, float]] = []
    for character in ("1", "0"):
        cell = Image.new("L", (char_width, char_height), 0)
        ImageDraw.Draw(cell).text((0, 0), character, fill=255, font=font)
        coverage = sum(cell.getdata()) / (255 * cell_area)
        measured.append((character, coverage))

    measured.sort(key=lambda item: item[1])
    max_density = measured[-1][1]
    if max_density <= 0:
        raise RuntimeError("Karakter yoğunluğu ölçülemedi.")

    return (
        (measured[0][0], 0),
        (measured[1][0], 255),
    )


def export_png(binary_art: list[str], output_path: str | Path) -> None:
    """Render binary art as white 0/1 characters on a black background.

    Args:
        binary_art: List of equal-length strings containing only '0' or '1'.
        output_path: Destination file path. Parent dirs are created if missing.

    Raises:
        ValueError: If the art is empty, rows have different lengths,
            or unsupported characters are used.
    """
    if not binary_art:
        raise ValueError("Portre boş olamaz.")

    col_count = len(binary_art[0])
    for i, row in enumerate(binary_art):
        if len(row) != col_count:
            raise ValueError(f"Satır {i} uzunluğu {len(row)}, beklenen {col_count}.")

    allowed_characters = {"0", "1"}
    used_characters = set("".join(binary_art))
    invalid_characters = used_characters - allowed_characters
    if invalid_characters:
        raise ValueError(f"Desteklenmeyen karakterler: {sorted(invalid_characters)}")

    font = _load_monospace_font(FONT_SIZE)
    char_width = max(1, ceil(font.getlength("M")))
    char_height = int(FONT_SIZE * 1.2)

    img_width = col_count * char_width
    img_height = len(binary_art) * char_height

    img = Image.new("RGB", (img_width, img_height), "black")
    draw = ImageDraw.Draw(img)

    for row_idx, row in enumerate(binary_art):
        y = row_idx * char_height
        draw.text((0, y), row, fill="white", font=font)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)
