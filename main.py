# SPDX-License-Identifier: MIT
"""Talvera passport page entry.

Copies the bundled artwork asset (asset.png, sitting beside this file) to
/output/entry.png. Fully deterministic, offline, no network, no randomness.

The artwork is an invented passport data page for the Republic of Talvera:
holder Elena Maris Voss, passport TV 4839201, issued 12 Mar 2023, expires
12 Mar 2033, with a portrait, a machine-readable strip, arrival/departure
stamps from Dravosk, Merren and Ostara (all dated after issue), and a red
HARBOUR TAX PAID 40 TALER stamp.
"""

import os
import shutil

ASSET_NAME = "asset.png"
OUTPUT_PATH = "/output/entry.png"
MAX_BYTES = 1_048_576
MAX_WIDTH = 1024
MAX_HEIGHT = 1024


def _check_png(path: str) -> None:
    """Assert the file is a whole PNG within the competition caps."""
    with open(path, "rb") as fh:
        head = fh.read(33)
    assert head[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG"
    assert head[12:16] == b"IHDR", "missing IHDR chunk"
    width = int.from_bytes(head[16:20], "big")
    height = int.from_bytes(head[20:24], "big")
    assert width <= MAX_WIDTH and height <= MAX_HEIGHT, (
        f"dimensions {width}x{height} exceed {MAX_WIDTH}x{MAX_HEIGHT}"
    )
    assert os.path.getsize(path) <= MAX_BYTES, "file exceeds 1 MiB"


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, ASSET_NAME)
    _check_png(src)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    shutil.copyfile(src, OUTPUT_PATH)
    _check_png(OUTPUT_PATH)


if __name__ == "__main__":
    main()
