#!/usr/bin/env python3
"""Create a new release folder from the TEMPLATE for a component.

Usage:
  python scripts/new_release.py hdf5-core 2.0.0
  python scripts/new_release.py hdfview 3.4.0
"""

from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
COMPONENTS = {"hdf5-core", "hdfview"}

def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__.strip())
        return 2

    comp, version = sys.argv[1], sys.argv[2]
    if comp not in COMPONENTS:
        print(f"ERROR: unknown component: {comp}")
        return 2

    src = ROOT / "proofs" / comp / "TEMPLATE"
    dst = ROOT / "proofs" / comp / version

    if dst.exists():
        print(f"ERROR: destination already exists: {dst}")
        return 1

    shutil.copytree(src, dst)
    print(f"Created: {dst}")
    print("Next: edit the new release index.md and replace PLACEHOLDER files with evidence.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
