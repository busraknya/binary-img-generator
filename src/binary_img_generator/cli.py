"""Command-line interface for Binary Image Generator."""

import argparse
import sys
from datetime import datetime
from pathlib import Path

from binary_img_generator.ascii_mapper import to_ascii
from binary_img_generator.grayscale import to_grayscale
from binary_img_generator.image_loader import load_image
from binary_img_generator.png_exporter import export_png


def _default_output_path() -> Path:
    """Timestamped default path so repeated runs don't overwrite each other."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return Path("output") / f"portre_{ts}.png"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="big",
        description="Fotoğrafı 0/1 karakterlerinden portreye çevirir.",
    )
    parser.add_argument("input", help="Girdi fotoğrafı (JPEG, PNG, WebP)")
    parser.add_argument(
        "--grid-width",
        type=int,
        default=120,
        help="Karakter genişliği (40-400, varsayılan 120)",
    )
    parser.add_argument(
        "--char-aspect",
        type=float,
        default=0.5,
        help="Karakter en/boy oranı (0.3-1.0, varsayılan 0.5)",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=128,
        help="Siyah/beyaz eşiği (0-255, varsayılan 128)",
    )
    parser.add_argument(
        "--invert",
        action="store_true",
        help="Siyah zemin yerine beyaz zemin kullan",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Çıktı dosyası (varsayılan: output/portre_<zaman>.png)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    output_path = args.output or _default_output_path()

    try:
        img = load_image(args.input)
        gray = to_grayscale(img)
        art = to_ascii(
            gray,
            grid_width=args.grid_width,
            char_aspect=args.char_aspect,
            threshold=args.threshold,
            invert=args.invert,
        )
        export_png(art, output_path)
    except (FileNotFoundError, ValueError) as exc:
        print(f"Hata: {exc}", file=sys.stderr)
        return 1

    print(f"Portre kaydedildi: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
