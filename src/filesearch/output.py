"""Terminal output: progress spinner and result formatting."""

import itertools
import sys

from .colors import Colors, highlight

_SPINNER_FRAMES = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
_CLEAR_LINE = "\r" + " " * 80 + "\r"


class ProgressSpinner:
    """In-place terminal spinner that shows scan progress."""

    def __init__(self) -> None:
        self._spinner = itertools.cycle(_SPINNER_FRAMES)
        self._active = Colors.ENABLED

    def update(self, files_checked: int, files_matched: int) -> None:
        if not self._active:
            return
        sys.stdout.write(
            f"\r  {Colors.CYAN}{next(self._spinner)}{Colors.RESET} "
            f"Scanning\u2026 {Colors.DIM}{files_checked} files checked, "
            f"{files_matched} matched{Colors.RESET}  "
        )
        sys.stdout.flush()

    def clear(self) -> None:
        if not self._active:
            return
        sys.stdout.write(_CLEAR_LINE)
        sys.stdout.flush()


def print_header(term: str, root: str, type_label: str, ignore_case: bool) -> None:
    """Print the search banner."""
    print(
        f"\n{Colors.BOLD}Searching {Colors.CYAN}{type_label}{Colors.RESET}"
        f"{Colors.BOLD} for {Colors.YELLOW}\"{term}\"{Colors.RESET}"
        f"{Colors.BOLD} in {Colors.CYAN}{root}{Colors.RESET}"
    )
    if ignore_case:
        print(f"{Colors.DIM}  (case-insensitive){Colors.RESET}")
    print(f"{Colors.DIM}{'─' * 70}{Colors.RESET}\n")


def print_match(filepath: str, matches: list[tuple[str, str]], term: str, ignore_case: bool) -> None:
    """Print a single file's matches immediately."""
    print(f"  {Colors.GREEN}{Colors.BOLD}{filepath}{Colors.RESET}")
    for label, line in matches:
        highlighted = highlight(line, term, ignore_case)
        print(f"    {Colors.DIM}{label}:{Colors.RESET} {highlighted}")
    print()


def print_summary(files_scanned: int, files_matched: int, total_matches: int) -> None:
    """Print the final statistics."""
    print(f"{Colors.DIM}{'─' * 70}{Colors.RESET}")
    print(f"  {Colors.BOLD}Files scanned: {Colors.RESET}{files_scanned}")
    print(f"  {Colors.BOLD}Files matched: {Colors.RESET}{Colors.YELLOW}{files_matched}{Colors.RESET}")
    print(f"  {Colors.BOLD}Total matches: {Colors.RESET}{Colors.YELLOW}{total_matches}{Colors.RESET}\n")
