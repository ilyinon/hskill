#!/usr/bin/env python3
"""Reassemble rectangular scans cut into PNG fragments with irregular seams."""

import argparse
import hashlib
from pathlib import Path
from zipfile import BadZipFile, ZipFile

try:
    import numpy as np
    from PIL import Image
except ImportError as exc:
    raise SystemExit("reassemble_png.py requires Pillow and NumPy") from exc


ROTATIONS = np.array([
    [[1, 0], [0, 1]], [[0, 1], [-1, 0]],
    [[-1, 0], [0, -1]], [[0, -1], [1, 0]],
])


def read_fragments(path):
    pieces = []
    with ZipFile(path) as archive:
        entries = sorted(
            (entry for entry in archive.infolist()
             if not entry.is_dir() and entry.filename.lower().endswith(".png")),
            key=lambda entry: entry.filename,
        )
        if not 2 <= len(entries) <= 40:
            raise ValueError("expected 2–40 PNG fragments")
        if len({entry.filename for entry in entries}) != len(entries):
            raise ValueError("duplicate ZIP member names")
        for entry in entries:
            if entry.file_size > 4 * 1024 * 1024:
                raise ValueError(f"{entry.filename}: PNG exceeds 4 MiB")
            with archive.open(entry) as source, Image.open(source, formats=["PNG"]) as image:
                if max(image.size) > 512 or image.n_frames != 1:
                    raise ValueError(f"{entry.filename}: expected a static PNG up to 512 px per side")
                rgba = image.convert("RGBA")
                alpha = rgba.getchannel("A")
                bounds = alpha.getbbox()
                if bounds is None or alpha.getextrema() != (0, 255):
                    raise ValueError(f"{entry.filename}: expected visible pixels and transparency")
                piece = np.asarray(rgba.crop(bounds))
                mask = piece[:, :, 3]
                if ((mask != 0) & (mask != 255)).any():
                    raise ValueError(f"{entry.filename}: expected a binary alpha mask")
                pieces.append(piece)
    return pieces


def contact_field(mask, size):
    field = np.zeros((size, size), dtype=np.float32)
    height, width = mask.shape
    field[:height, :width] = -12 * mask.astype(np.float32)
    for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        rows = (np.arange(height) + dy) % size
        cols = (np.arange(width) + dx) % size
        field[np.ix_(rows, cols)] += mask
    return np.fft.rfft2(field)


def is_irregular_seam(mask, rotated, x, y):
    height, width = mask.shape
    top, left = max(y, 0), max(x, 0)
    bottom = min(y + rotated.shape[0], height)
    right = min(x + rotated.shape[1], width)
    if top >= bottom or left >= right:
        return False
    here = np.s_[top:bottom, left:right]
    candidate = rotated[top-y:bottom-y, left-x:right-x]
    if np.any(candidate & mask[here]):
        return False

    padded = np.pad(mask, 1)
    sides = (padded[:-2, 1:-1], padded[2:, 1:-1], padded[1:-1, :-2], padded[1:-1, 2:])
    # Require two directions of contact to reject straight outer edges.
    return sum(np.count_nonzero(candidate & side[here]) >= 6 for side in sides) >= 2


def find_seams(masks):
    max_side = max(max(mask.shape) for mask in masks)
    size = (2 * max_side + 33) // 32 * 32
    spectra = [
        [np.fft.rfft2(np.rot90(mask, k).astype(np.float32),
                       s=(size, size), axes=(0, 1)).conj().astype(np.complex64)
         for k in range(4)]
        for mask in masks
    ]
    seams = []
    for i, mask in enumerate(masks):
        weighted = contact_field(mask, size)
        for j in range(i + 1, len(masks)):
            for k, spectrum in enumerate(spectra[j]):
                scores = np.fft.irfft2(weighted * spectrum, s=(size, size), axes=(0, 1))
                row, col = np.unravel_index(scores.argmax(), scores.shape)
                x = int((col + size // 2) % size - size // 2)
                y = int((row + size // 2) % size - size // 2)
                if is_irregular_seam(mask, np.rot90(masks[j], k), x, y):
                    seams.append((round(float(scores[row, col])), i, j, k, x, y))
    return sorted(seams, reverse=True)


def place_fragments(masks, seams):
    links = [[] for _ in masks]
    components = list(range(len(masks)))
    for _, i, j, turns, x, y in seams:
        if components[i] == components[j]:
            continue
        height, width = masks[j].shape
        offsets = ((0, 0), (0, width - 1), (width - 1, height - 1), (height - 1, 0))
        rotation = ROTATIONS[turns]
        offset = np.array(offsets[turns]) + (x, y)
        links[i].append((j, rotation, offset))
        links[j].append((i, rotation.T, -rotation.T @ offset))
        old_component = components[j]
        components = [components[i] if value == old_component else value for value in components]

    placed = {0: (ROTATIONS[0], np.zeros(2, dtype=int))}
    pending = [0]
    while pending:
        i = pending.pop()
        rotation, offset = placed[i]
        for j, relative_rotation, relative_offset in links[i]:
            if j not in placed:
                placed[j] = (rotation @ relative_rotation, offset + rotation @ relative_offset)
                pending.append(j)
    if len(placed) != len(masks):
        raise ValueError(f"assembly incomplete: connected {len(placed)} of {len(masks)} fragments")
    return placed


def reconstruct(pieces):
    masks = [piece[:, :, 3] == 255 for piece in pieces]
    positions = place_fragments(masks, find_seams(masks))
    points, colors = [], []
    for i, piece in enumerate(pieces):
        y, x = np.where(masks[i])
        rotation, offset = positions[i]
        points.append(rotation @ np.stack((x, y)) + offset[:, None])
        colors.append(piece[y, x, :3])

    x, y = np.concatenate(points, axis=1)
    x -= x.min()
    y -= y.min()
    width, height = int(x.max() + 1), int(y.max() + 1)
    if width * height != x.size or np.unique(y * width + x).size != x.size:
        raise ValueError("assembly incomplete: rectangle has gaps or overlapping pixels")
    rgb = np.empty((height, width, 3), dtype=np.uint8)
    rgb[y, x] = np.concatenate(colors)
    return Image.fromarray(rgb)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path, help="ZIP containing PNG fragments")
    parser.add_argument("output", type=Path, help="path to a new PNG")
    parser.add_argument("--sha256", help="expected archive SHA-256")
    parser.add_argument("--rotate", type=int, choices=(0, 90, 180, 270), default=0,
                        help="rotate the result counterclockwise")
    args = parser.parse_args()
    try:
        if args.output.exists():
            raise ValueError(f"output already exists: {args.output}")
        if args.sha256:
            digest = hashlib.sha256()
            with args.archive.open("rb") as source:
                for block in iter(lambda: source.read(64 * 1024), b""):
                    digest.update(block)
            if digest.hexdigest() != args.sha256.lower():
                raise ValueError("archive SHA-256 mismatch")
        pieces = read_fragments(args.archive)
        image = reconstruct(pieces).rotate(args.rotate, expand=True)
        with args.output.open("xb") as target:
            image.save(target, format="PNG")
    except (BadZipFile, OSError, RuntimeError, ValueError) as exc:
        parser.exit(1, f"{exc}\n")
    print(f"{len(pieces)} fragments, {image.width}x{image.height}, no gaps or overlaps")


if __name__ == "__main__":
    main()
