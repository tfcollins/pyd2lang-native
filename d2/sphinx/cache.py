"""Content-hash cache for compiled D2 SVGs.

Keyed on (source, library, theme, d2.__version__) so a library version
bump invalidates all entries automatically. Null-byte separators prevent
boundary-collision false hits between adjacent fields.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


def make_key(source: str, library: str | None, theme: str, version: str) -> str:
    parts = [source, str(library), theme, version]
    data = "\x00".join(parts).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def cache_path(cache_dir: Path, key: str) -> Path:
    return Path(cache_dir) / key[:2] / f"{key}.svg"


def get(cache_dir: Path, key: str) -> str | None:
    path = cache_path(cache_dir, key)
    if path.is_file():
        return path.read_text(encoding="utf-8")
    return None


def put(cache_dir: Path, key: str, svg: str) -> None:
    path = cache_path(cache_dir, key)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg, encoding="utf-8")
