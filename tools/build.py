#!/usr/bin/env python3
"""Build index.html from src/index.src.html, embedding every luts/*.cube as a built-in filter.

Usage:  python3 tools/build.py
Uses only the Python standard library.
"""
import base64, json, re, struct, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "index.src.html"
OUT = ROOT / "index.html"
PLACEHOLDER = "/*__BUILTIN__*/[]"


def read_cube(path: Path):
    size, vals = 0, []
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        up = line.upper()
        if up.startswith("LUT_3D_SIZE"):
            size = int(line.split()[1])
            continue
        if re.match(r"^[A-Z_]", up):
            continue
        parts = line.split()
        if len(parts) >= 3:
            vals.extend(float(v) for v in parts[:3])
    if not size or len(vals) < size ** 3 * 3:
        raise ValueError(f"{path.name}: not a valid 3D LUT")
    vals = vals[: size ** 3 * 3]
    packed = struct.pack("<%dH" % len(vals), *(round(min(1, max(0, v)) * 65535) for v in vals))
    return size, base64.b64encode(packed).decode()


def pretty(stem: str) -> str:
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", stem).replace("_", " ").replace("-", " ").strip()


def main():
    src = SRC.read_text()
    if PLACEHOLDER not in src:
        sys.exit("Built-in placeholder not found in src/index.src.html")
    items = []
    for cube in sorted((ROOT / "luts").glob("*.cube")):
        size, data = read_cube(cube)
        items.append({"id": "b-" + re.sub(r"[^a-z0-9]+", "", cube.stem.lower()),
                      "name": pretty(cube.stem), "size": size, "data": data})
        print(f"  + {pretty(cube.stem)} ({size}³)")
    OUT.write_text(src.replace(PLACEHOLDER, json.dumps(items)))
    print(f"Built index.html · {len(items)} built-in filters · {OUT.stat().st_size/1024:.0f} KB")


if __name__ == "__main__":
    main()
