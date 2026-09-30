"""Filesystem locations that work both from source and from a frozen .exe.

- resources(): bundled read-only files (assets/, fonts/, prebuilt .synth/).
  When frozen by PyInstaller this is the extracted bundle dir (sys._MEIPASS).
- user_data(): writable files (progress.json, generated .synth/).
  When frozen this is the folder the .exe lives in, so saves persist.
"""
import sys
from pathlib import Path


def frozen():
    return getattr(sys, "frozen", False)


def resources():
    if frozen():
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent


def user_data():
    if frozen():
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent
