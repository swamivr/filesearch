"""Search strategies for different file types."""

import logging
from pathlib import Path

from pypdf import PdfReader

# Suppress noisy pypdf warnings (e.g. "Ignoring wrong pointing object")
logging.getLogger("pypdf").setLevel(logging.ERROR)


def search_pdf(filepath: Path, term: str, ignore_case: bool) -> list[tuple[str, str]]:
    """Extract text from a PDF and return matching lines.

    Returns a list of ``(location_label, line_text)`` tuples where
    *location_label* is the page number (e.g. ``"p.   3"``).
    """
    matches: list[tuple[str, str]] = []
    try:
        reader = PdfReader(filepath)
        for page_num, page in enumerate(reader.pages, start=1):
            text = page.extract_text()
            if not text:
                continue
            for line in text.splitlines():
                compare_line = line.lower() if ignore_case else line
                compare_term = term.lower() if ignore_case else term
                if compare_term in compare_line:
                    matches.append((f"p.{page_num:>4}", line.strip()))
    except Exception:
        pass
    return matches


def search_text_file(filepath: Path, term: str, ignore_case: bool) -> list[tuple[str, str]]:
    """Search a plain-text file line by line.

    Returns a list of ``(location_label, line_text)`` tuples where
    *location_label* is the line number.
    """
    matches: list[tuple[str, str]] = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            for lineno, line in enumerate(f, start=1):
                compare_line = line.lower() if ignore_case else line
                compare_term = term.lower() if ignore_case else term
                if compare_term in compare_line:
                    matches.append((f"{lineno:>5}", line.rstrip("\n\r")))
    except (OSError, PermissionError):
        pass
    return matches


def search_file(filepath: Path, term: str, ignore_case: bool) -> list[tuple[str, str]]:
    """Dispatch to the right searcher based on file extension."""
    if filepath.suffix.lower() == ".pdf":
        return search_pdf(filepath, term, ignore_case)
    return search_text_file(filepath, term, ignore_case)
