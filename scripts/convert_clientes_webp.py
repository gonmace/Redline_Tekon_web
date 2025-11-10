#!/usr/bin/env python3
"""
Normalize client logo images.

Usage:
    python scripts/convert_clientes_webp.py [--dry-run]

The script reads every image found in `source/clientes`, resizes it so the
resulting height is at most 120px (keeping the aspect ratio) and stores the
output as WEBP in `source/clientes_webp`.
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from PIL import Image, ImageOps

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_DIR = BASE_DIR / "source" / "clientes"
OUTPUT_DIR = BASE_DIR / "source" / "clientes_webp"
MAX_HEIGHT = 120
SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}


def iter_input_files():
    for path in sorted(INPUT_DIR.glob("*")):
        if path.suffix.lower() in SUPPORTED_EXTENSIONS and path.is_file():
            yield path


def convert_image(path: Path, dry_run: bool = False) -> Path | None:
    relative_name = path.relative_to(INPUT_DIR)
    output_path = OUTPUT_DIR / relative_name.with_suffix(".webp")

    logging.info("Processing %s -> %s", path.name, output_path.name)

    if dry_run:
        return output_path

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(path) as img:
        img = ImageOps.exif_transpose(img)

        width, height = img.size
        if height > MAX_HEIGHT:
            ratio = MAX_HEIGHT / height
            new_size = (int(round(width * ratio)), MAX_HEIGHT)
            img = img.resize(new_size, Image.LANCZOS)
        else:
            new_size = (width, height)

        if img.mode not in {"RGB", "RGBA"}:
            img = img.convert("RGBA")

        img.save(
            output_path,
            format="WEBP",
            quality=90,
            method=6,
            lossless=False,
        )

    logging.debug(
        "Saved %s with size %sx%s", output_path.name, *new_size
    )
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Normalize client logos to 120px height and WEBP format."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the files that would be processed without writing output.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only display warnings and errors.",
    )
    args = parser.parse_args()

    log_level = logging.WARNING if args.quiet else logging.INFO
    logging.basicConfig(format="%(message)s", level=log_level)

    if not INPUT_DIR.exists():
        raise SystemExit(f"Input directory not found: {INPUT_DIR}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    processed = 0
    for file_path in iter_input_files():
        convert_image(file_path, dry_run=args.dry_run)
        processed += 1

    logging.info(
        "%s %s processed.",
        processed,
        "file was" if processed == 1 else "files were",
    )


if __name__ == "__main__":
    main()

