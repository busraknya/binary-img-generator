"""Allow running as `python -m binary_img_generator`."""

import sys

from binary_img_generator.cli import main

if __name__ == "__main__":
    sys.exit(main())
