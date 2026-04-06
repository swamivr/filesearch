"""File-system walking and binary detection."""

import os
from pathlib import Path

# Known binary extensions — skipped when searching all file types (``-t "*"``).
BINARY_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".svg", ".webp",
    ".mp3", ".mp4", ".avi", ".mov", ".mkv", ".flac", ".wav",
    ".zip", ".tar", ".gz", ".bz2", ".7z", ".rar",
    ".exe", ".dll", ".so", ".dylib", ".bin", ".o", ".obj",
    ".doc", ".xls", ".ppt",
    ".pyc", ".pyo", ".class", ".wasm",
    ".ttf", ".otf", ".woff", ".woff2",
    ".sqlite", ".db",
}

_BINARY_CHECK_SIZE = 8192


def is_binary(filepath: Path) -> bool:
    """Return ``True`` if *filepath* looks like a binary file (contains null bytes)."""
    try:
        with open(filepath, "rb") as f:
            return b"\x00" in f.read(_BINARY_CHECK_SIZE)
    except (OSError, PermissionError):
        return True


def walk_files(
    root: Path,
    ext_filter: str | None,
    max_depth: int | None,
):
    """Yield candidate file paths under *root*.

    Parameters
    ----------
    root:
        Directory to search.
    ext_filter:
        A single extension including the dot (e.g. ``".pdf"``),
        or ``None`` to match all non-binary files.
    max_depth:
        Maximum directory depth relative to *root*.  ``None`` means unlimited.
    """
    root = root.resolve()

    for dirpath, dirnames, filenames in os.walk(root):
        if max_depth is not None:
            depth = Path(dirpath).resolve().relative_to(root).parts
            if len(depth) > max_depth:
                dirnames.clear()
                continue

        # Skip hidden directories
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]

        for fname in filenames:
            if fname.startswith("."):
                continue

            fpath = Path(dirpath) / fname
            ext = fpath.suffix.lower()

            # Specific extension filter
            if ext_filter is not None and ext != ext_filter:
                continue

            # When searching all (*), skip known binary formats (PDFs handled separately)
            if ext_filter is None and ext in BINARY_EXTENSIONS:
                continue

            # For non-PDF files when searching all, skip binary content
            if ext_filter is None and ext != ".pdf" and is_binary(fpath):
                continue

            yield fpath
