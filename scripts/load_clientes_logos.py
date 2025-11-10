#!/usr/bin/env python3
"""
Load client logos into the `Cliente` model.

For every image contained in `source/clientes_webp` (or `source/clientes` as
fallback) the script will:
  * Resize the image so that its height is at most 120px (keeping aspect ratio)
  * Convert it to WEBP
  * Store the resulting file inside `media/clientes`
  * Create or update the corresponding `Cliente` entry with the generated logo

Usage:
    source venv/bin/activate
    python scripts/load_clientes_logos.py [--dry-run] [--overwrite]
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from io import BytesIO
from pathlib import Path
from typing import Iterable

import django
from PIL import Image, ImageOps

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tekon_website.settings")
django.setup()

from django.core.files.base import ContentFile  # noqa: E402
from django.utils.text import slugify  # noqa: E402

from empresa.models import Cliente  # noqa: E402

WEBP_SOURCE = BASE_DIR / "source" / "clientes_webp"
FALLBACK_SOURCE = BASE_DIR / "source" / "clientes"
MAX_HEIGHT = 120

NAME_OVERRIDES = {
    "applus": "Applus",
    "belmonte": "Belmonte Ingenieros SRL",
    "cambridge": "Cambridge College",
    "cambridge2": "Cambridge College",
    "citsa": "CITSA",
    "citsa2": "CITSA",
    "doisa": "DOISA",
    "doisa2": "DOISA",
    "embol": "Embol",
    "embol2": "Embol",
    "ende andina": "ENDE Andina",
    "ende guarachachi": "ENDE Guaracachi",
    "gadcochabamba": "GAD Cochabamba",
    "gas energy": "Gas Energy",
    "ghenova": "Ghenova",
    "gme towers": "GME Towers",
    "ingerut": "Ingerut",
    "ipebolivia": "IPE Bolivia",
    "mopsv": "MOPSV",
    "myd unidos": "M&D Unidos",
    "petrobras": "Petrobras",
    "prodiel": "Prodiel",
    "pti": "Phoenix Tower International",
    "puertas": "Puertas",
    "serpetbol": "Serpetbol",
    "spacex": "SpaceX",
    "spacex2": "SpaceX",
    "sts": "STS",
    "transredes": "Transredes",
    "tunari": "Tunari",
    "vestas": "Vestas",
    "ypfb chaco": "YPFB Chaco",
    "ypfb corp": "YPFB Corporación",
    "ypfb transporte": "YPFB Transporte",
}

TYPE_OVERRIDES = {
    "M&D Unidos": "final",
    "Belmonte Ingenieros SRL": "final",
}


def iter_image_files(directory: Path) -> Iterable[Path]:
    for path in sorted(directory.glob("*")):
        if path.is_file():
            yield path


def humanize_name(stem: str) -> str:
    base_key = re.sub(r"\s+", " ", stem.lower()).strip()
    name = NAME_OVERRIDES.get(base_key)
    if name:
        return name

    base_key = re.sub(r"\d+$", "", base_key).strip()
    name = NAME_OVERRIDES.get(base_key)
    if name:
        return name

    words = re.split(r"[\s_-]+", stem)
    processed = []
    for word in words:
        if not word:
            continue
        if word.isupper():
            processed.append(word)
        elif len(word) <= 3:
            processed.append(word.upper())
        else:
            processed.append(word.capitalize())
    return " ".join(processed) or stem


def build_webp_bytes(path: Path) -> BytesIO:
    with Image.open(path) as img:
        img = ImageOps.exif_transpose(img)
        width, height = img.size
        if height > MAX_HEIGHT:
            ratio = MAX_HEIGHT / height
            new_size = (int(round(width * ratio)), MAX_HEIGHT)
            img = img.resize(new_size, Image.LANCZOS)

        if img.mode not in {"RGB", "RGBA"}:
            img = img.convert("RGBA")

        buffer = BytesIO()
        img.save(
            buffer,
            format="WEBP",
            quality=90,
            method=6,
            lossless=False,
        )
        buffer.seek(0)
        return buffer


def load_logo(image_path: Path, overwrite: bool = False, dry_run: bool = False) -> None:
    stem = image_path.stem
    stem_key = re.sub(r"\d+$", "", stem).lower()
    name = humanize_name(stem)

    cliente = Cliente.objects.filter(nombre__iexact=name).first()
    if not cliente:
        cliente = Cliente(nombre=name)
        cliente.tipo_cliente = TYPE_OVERRIDES.get(name, "directo")
        cliente.descripcion = cliente.descripcion or ""
        cliente.activo = True

    if cliente.logo:
        if not overwrite:
            return
        if not dry_run:
            cliente.logo.delete(save=False)

    slug = slugify(name) or slugify(stem) or stem.lower()
    file_name = f"{slug}.webp"

    if dry_run:
        print(f"[DRY-RUN] Would assign {image_path.name} -> {name}")
        return

    webp_content = build_webp_bytes(image_path)
    cliente.logo.save(file_name, ContentFile(webp_content.read()), save=False)
    cliente.tipo_cliente = TYPE_OVERRIDES.get(name, cliente.tipo_cliente or "directo")
    cliente.activo = True
    cliente.save()
    print(f"Asignado logo {image_path.name} al cliente '{cliente.nombre}'")


def main() -> None:
    parser = argparse.ArgumentParser(description="Load client logos into the database.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the actions that would be performed without touching the database.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing logos if the client already has one assigned.",
    )
    args = parser.parse_args()

    source_dir = WEBP_SOURCE if WEBP_SOURCE.exists() else FALLBACK_SOURCE
    if not source_dir.exists():
        raise SystemExit(f"No se encontró el directorio de logos: {source_dir}")

    seen_keys: set[str] = set()
    for image_path in iter_image_files(source_dir):
        base_key = re.sub(r"\d+$", "", image_path.stem).lower()
        if base_key in seen_keys:
            continue
        seen_keys.add(base_key)
        load_logo(image_path, overwrite=args.overwrite, dry_run=args.dry_run)


if __name__ == "__main__":
    main()

