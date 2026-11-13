"""Export ASCII art as a PNG image."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Font size in pixels. At 20px with monospace, 120 chars ≈ 1440px wide,
# which satisfies BR-06 (min 1200px output).
FONT_SIZE = 20

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


def export_png(ascii_art: list[str], output_path: str | Path) -> None:
    """Render ASCII art as a PNG file (white '1's on black background).

    Args:
        ascii_art: List of equal-length strings, each char '1' or ' '.
        output_path: Destination file path. Parent dirs are created if missing.

    Raises:
        ValueError: If ascii_art is empty or rows have different lengths.
    """
    if not ascii_art:
        raise ValueError("Portre boş olamaz.")

    col_count = len(ascii_art[0])
    for i, row in enumerate(ascii_art):
        if len(row) != col_count:
            raise ValueError(f"Satır {i} uzunluğu {len(row)}, beklenen {col_count}.")

    font = _load_monospace_font(FONT_SIZE)
    char_width = int(font.getlength("M"))
    # Vertical spacing slightly larger than font size so rows don't overlap.
    char_height = int(FONT_SIZE * 1.2)

    img_width = col_count * char_width
    img_height = len(ascii_art) * char_height

    img = Image.new("RGB", (img_width, img_height), "black")
    draw = ImageDraw.Draw(img)

    # One draw call per row (fast); the '1's in each row become white text.
    for row_idx, row in enumerate(ascii_art):
        y = row_idx * char_height
        draw.text((0, y), row, fill="white", font=font)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path)
