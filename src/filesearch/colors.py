"""ANSI color codes and text highlighting."""

import os
import re
import sys


def _ansi_supported() -> bool:
    """Check if the terminal supports ANSI escape codes."""
    if not sys.stdout.isatty():
        return False
    # Windows CMD/PowerShell: enable ANSI via Virtual Terminal Processing
    if os.name == "nt":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32  # type: ignore[attr-defined]
            # STD_OUTPUT_HANDLE = -11
            handle = kernel32.GetStdHandle(-11)
            # Get current mode
            mode = ctypes.c_ulong()
            kernel32.GetConsoleMode(handle, ctypes.byref(mode))
            # ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)
            return True
        except Exception:
            return False
    return True


class Colors:
    """ANSI color codes (disabled automatically if output is not a terminal)."""

    ENABLED = _ansi_supported()

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
