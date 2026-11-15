"""Allow running as `python -m binary_img_generator`."""

import sys

from binary_img_generator.cli import main

if __name__ == "__main__":
    sys.exit(main())

art = to_ascii(
    gray,
    grid_width=args.grid_width,
    char_aspect=args.char_aspect,
    threshold=args.threshold,
    invert=args.invert,
    dither=args.dither,  # ← ekle
)
