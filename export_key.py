"""Export keycap sprites in every world palette.

Usage: python export_key.py [KEY] [scale]
  KEY   keycap name, e.g. A, D, SPACE, UP (default: A)
  scale pixel scale factor (default: 4)

Writes exports/<key>_key_autumn.png, ..._winter.png, ..._ember.png
next to this script.
"""
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
import sys
from pathlib import Path

import pygame

pygame.init()
pygame.display.set_mode((64, 64))

from game import gui, sprites


def main():
    key = (sys.argv[1] if len(sys.argv) > 1 else "A").upper()
    try:
        k = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    except ValueError:
        k = 4
    outdir = Path(__file__).resolve().parent / "exports"
    outdir.mkdir(exist_ok=True)
    for theme in ("autumn", "winter", "ember"):
        gui.set_theme(theme)
        img = sprites.key(key, k=k)
        path = outdir / f"{key.lower()}_key_{theme}.png"
        pygame.image.save(img, str(path))
        print("saved", path)


if __name__ == "__main__":
    main()
