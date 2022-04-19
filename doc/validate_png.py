"""Validate the PNG images in the build/latex/ directory.

Removes invalid PNGs (probably GIF)
"""
from glob import glob
import os

from PIL import Image

this_path = os.path.dirname(os.path.abspath(__file__))
check_path = os.path.join(this_path, "build", "latex")
if not os.path.isdir(check_path):
    raise FileNotFoundError(f"Invalid path {check_path}")

for filename in glob(os.path.join(check_path, "*.png")):
    im = Image.open(filename)
    im.save(filename, format="png")
    im.close()  # reload is necessary in my case
