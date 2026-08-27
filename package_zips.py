#!/usr/bin/env python3
"""Build and package day-wise training artifacts into clean ZIP archives.

Usage:
    python package_zips.py
    # or
    uv run python package_zips.py
"""

import os
import sys
import zipfile
import time
from pathlib import Path

# Directories/files to ignore during packaging
IGNORE_PATTERNS = {
    "__pycache__",
    ".pytest_cache",
    ".DS_Store",
    ".venv",
    ".git",
    "*.pyc",
    "*.pyo"
}


def should_ignore(path: Path) -> bool:
    """Check if file/folder matches any ignore pattern."""
    for part in path.parts:
        if part in IGNORE_PATTERNS or part.endswith((".pyc", ".pyo")):
            return True
    return False


def build_day_zip(day_dir: Path, output_zip: Path) -> tuple[int, int]:
    """Compresses a day directory into a zip file, excluding cache files."""
    file_count = 0
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(day_dir):
            # Prune ignored directories in-place
            dirs[:] = [d for d in dirs if not should_ignore(Path(root) / d)]
            
            for file in files:
                file_path = Path(root) / file
                if not should_ignore(file_path):
                    # Store relative to workspace root (e.g. day-01/slides.html)
                    arcname = file_path.relative_to(day_dir.parent)
                    zipf.write(file_path, arcname)
                    file_count += 1

    size_bytes = output_zip.stat().st_size
    return file_count, size_bytes


def main():
    root_dir = Path(__file__).resolve().parent
    day_dirs = sorted([d for d in root_dir.iterdir() if d.is_dir() and d.name.startswith("day-")])

    if not day_dirs:
        print("[ERROR] No day directories found (e.g. day-01, day-02).")
        sys.exit(1)

    print("=" * 65)
    print("📦  PACKAGING DAY-WISE ARTIFACT ZIP ARCHIVES")
    print("=" * 65)

    start_time = time.perf_counter()
    total_files = 0
    total_size = 0

    for day_dir in day_dirs:
        zip_name = f"{day_dir.name}.zip"
        zip_path = root_dir / zip_name
        
        file_count, size_bytes = build_day_zip(day_dir, zip_path)
        total_files += file_count
        total_size += size_bytes
        
        size_kb = size_bytes / 1024
        print(f" ✓  {zip_name:<14} -> {file_count:>2} files | {size_kb:6.1f} KB")

    elapsed = time.perf_counter() - start_time
    print("-" * 65)
    print(f"🎉 Successfully updated {len(day_dirs)} ZIP archives ({total_files} total files, {total_size/1024:.1f} KB) in {elapsed:.2f}s.")
    print("=" * 65)


if __name__ == "__main__":
    main()
