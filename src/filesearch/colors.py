"""ANSI color codes and text highlighting."""

import re
import sys


class Colors:
    """ANSI color codes (disabled automatically if output is not a terminal)."""

    ENABLED = sys.stdout.isatty()

    RESET  = "\033[0m"  if ENABLED else ""
    BOLD   = "\033[1m"  if ENABLED else ""
    GREEN  = "\033[32m" if ENABLED else ""
    CYAN   = "\033[36m" if ENABLED else ""
    YELLOW = "\033[33m" if ENABLED else ""
    RED    = "\033[31m" if ENABLED else ""
    DIM    = "\033[2m"  if ENABLED else ""


def highlight(text: str, term: str, ignore_case: bool) -> str:
    """Highlight all occurrences of *term* inside *text* with red+bold."""
    if not Colors.ENABLED:
        return text
    flags = re.IGNORECASE if ignore_case else 0
    pattern = re.compile(re.escape(term), flags)
    return pattern.sub(
        lambda m: f"{Colors.RED}{Colors.BOLD}{m.group()}{Colors.RESET}", text
    )
