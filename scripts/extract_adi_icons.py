"""One-shot migration: decode the base64 blobs in lib/adi/adi-components.d2
into source SVG files under lib/adi/icons/, then verify the new generator
round-trips losslessly.

Run once:

    python scripts/extract_adi_icons.py

After a successful run, commit lib/adi/icons/*.svg and the updated header
in lib/adi/adi-components.d2.
"""

from __future__ import annotations

import base64
import re
import subprocess
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_ADI_D2 = _ROOT / "lib" / "adi" / "adi-components.d2"
_ICONS_DIR = _ROOT / "lib" / "adi" / "icons"

_ENTRY_RE = re.compile(
    r'^\s{2}(?P<name>[a-z][a-z0-9-]*):\s*\{\s*\n'
    r'^\s{4}icon:\s*"data:image/svg\+xml;base64,(?P<b64>[A-Za-z0-9+/=]+)"\s*\n'
    r'^\s{2}\}\s*\n',
    re.MULTILINE,
)


def _parse_entries(d2_text: str) -> dict[str, str]:
    return {m.group("name"): m.group("b64") for m in _ENTRY_RE.finditer(d2_text)}


def main() -> int:
    before = _parse_entries(_ADI_D2.read_text())
    if not before:
        print(f"ERROR: no icon entries found in {_ADI_D2}", file=sys.stderr)
        return 1

    _ICONS_DIR.mkdir(parents=True, exist_ok=True)
    for name, b64 in before.items():
        (_ICONS_DIR / f"{name}.svg").write_bytes(base64.b64decode(b64))
    print(f"Extracted {len(before)} icons to {_ICONS_DIR}")

    # Run the generator in write mode so the header updates to reference
    # the new script.
    result = subprocess.run(
        [sys.executable, "scripts/embed_icons.py", "--library", "adi"],
        cwd=_ROOT,
    )
    if result.returncode != 0:
        print("ERROR: embed_icons.py failed during regeneration", file=sys.stderr)
        return 1

    # Verify body base64 content is byte-identical (header may differ).
    after = _parse_entries(_ADI_D2.read_text())
    missing = set(before) - set(after)
    extra = set(after) - set(before)
    differ = {k for k in before if k in after and before[k] != after[k]}
    if missing or extra or differ:
        print(
            "ERROR: round-trip failed — "
            f"missing={sorted(missing)} extra={sorted(extra)} differ={sorted(differ)}",
            file=sys.stderr,
        )
        return 1

    print("Regen round-trips: OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
