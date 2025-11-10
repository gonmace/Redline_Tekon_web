#!/usr/bin/env python3
"""Upscale client WEBP logos to a minimum height of 120px."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageOps

BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_DIR = BASE_DIR / "source" / "clientes_webp"
TARGET_HEIGHT = 120
SUPPORTED_EXTENSIONS = {".webp"}


def iter_images():
    for path in sorted(INPUT_DIR.glob("*")):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            yield path


def ensure_height(path: Path, dry_run: bool = False) -> bool:
    with Image.open(path) as img:
        img = ImageOps.exif_transpose(img)
        width, height = img.size

        if height >= TARGET_HEIGHT:
            return False

        ratio = TARGET_HEIGHT / height
        new_size = (int(round(width * ratio)), TARGET_HEIGHT)

        if dry_run:
            print(f"[DRY-RUN] Would upscale {path.name} from {width}x{height} to {new_size[0]}x{new_size[1]}")
            return True

        resized = img.resize(new_size, Image.LANCZOS)

        if resized.mode not in {"RGB", "RGBA"}:
            resized = resized.convert("RGBA")

        resized.save(path, format="WEBP", quality=95, method=6, lossless=False)
        print(f"Upscaled {path.name} -> {new_size[0]}x{new_size[1]}")
        return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Ensure client WEBP logos have at least 120px height by upscaling if needed."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the changes that would be performed without modifying files.",
    )
    args = parser.parse_args()

    if not INPUT_DIR.exists():
        raise SystemExit(f"No se encontró el directorio de logos: {INPUT_DIR}")

    processed = 0
    for image_path in iter_images():
        if ensure_height(image_path, dry_run=args.dry_run):
            processed += 1

    suffix = " (dry-run)" if args.dry_run else ""
    print(f"{processed} archivo(s) ajustados{suffix}.")


if __name__ == "__main__":
    main()
