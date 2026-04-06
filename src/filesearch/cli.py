"""Command-line interface — argument parsing and main orchestration."""

import argparse
import os
import sys
from pathlib import Path

from .colors import Colors
from .output import ProgressSpinner, print_header, print_match, print_summary
from .searchers import search_file
from .walker import walk_files


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    from . import __version__

    parser = argparse.ArgumentParser(
        prog="filesearch",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""\
filesearch — recursively search files for a word or phrase.

Scans all files of a given type inside a folder (and its subfolders) for
lines that contain the search term. PDF files are read with a PDF text
extractor; every other file type is read as plain text. Matching lines
are printed immediately as they are found, along with a progress spinner.

Supported file types:
  pdf (default)   Extracts text from each page using pypdf.
  txt, csv, log,  Read as plain UTF-8 text; any extension works.
  py, js, …
  *               Search ALL non-binary files regardless of extension.""",
        epilog="""\
examples:
  filesearch "invoice"                          Search PDFs in current directory
  filesearch "invoice" ./docs                   Search PDFs in ./docs
  filesearch "TODO" ./src -t py                 Search Python files in ./src
  filesearch "error" /var/logs -t log -i        Case-insensitive in .log files
  filesearch "import os" . -t "*"               Search all non-binary files
  filesearch "config" . -t yaml --max-depth 2   Limit to 2 levels deep

output:
  For each matching file the full path is printed, followed by every
  matching line. PDF matches show the page number (p.  1:), text files
  show the line number (   42:). A summary of files scanned, files
  matched, and total matches is printed at the end.""",
    )

    parser.add_argument(
        "search_term",
        help="The word or phrase to search for. Use quotes around multi-word "
             'terms, e.g. "hello world".',
    )
    parser.add_argument(
        "folder", nargs="?", default=".",
        help="Root folder to search. The search includes all subfolders "
             "recursively. Defaults to the current working directory (.).",
    )
    parser.add_argument(
        "-t", "--type", default="pdf", dest="filetype", metavar="TYPE",
        help="File extension to filter by (without the dot). Examples: pdf, "
             "txt, csv, py, log, json, yaml. Use * to search all non-binary "
             "files. Default: pdf.",
    )
    parser.add_argument(
        "-i", "--ignore-case", action="store_true",
        help='Match the search term regardless of upper/lower case. '
             'e.g. "error" will also match "Error" and "ERROR".',
    )
    parser.add_argument(
        "--max-depth", type=int, default=None, metavar="N",
        help="Limit how many levels of subfolders to descend into. "
             "0 means only the root folder itself, 1 includes its immediate "
             "children, etc. By default there is no limit.",
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version=f"%(prog)s {__version__}",
        help="Show the program version and exit.",
    )

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    """Entry point for the CLI."""
    args = parse_args(argv)

    folder = args.folder
    # On Windows, ensure UNC paths keep their leading backslashes.
    # CMD can swallow a layer of backslashes, so accept both \\ and raw \ prefix.
    if os.name == "nt" and folder.startswith("\\") and not folder.startswith("\\\\"):
        folder = "\\" + folder  # restore the missing leading backslash

    root = Path(folder)
    if not root.is_dir():
        print(f"{Colors.RED}Error: '{folder}' is not a valid directory.{Colors.RESET}")
        sys.exit(1)

    term = args.search_term
    filetype = args.filetype.strip().lstrip(".")

    if filetype == "*":
        ext_filter = None
        type_label = "all files"
    else:
        ext_filter = f".{filetype.lower()}"
        type_label = f".{filetype} files"

    total_files_scanned = 0
    total_files_matched = 0
    total_matches = 0

    print_header(term, str(root.resolve()), type_label, args.ignore_case)

    spinner = ProgressSpinner()

    for fpath in walk_files(root, ext_filter, args.max_depth):
        total_files_scanned += 1
        spinner.update(total_files_scanned, total_files_matched)

        matches = search_file(fpath, term, args.ignore_case)

        if matches:
            total_files_matched += 1
            total_matches += len(matches)

            spinner.clear()
            print_match(str(fpath), matches, term, args.ignore_case)

    spinner.clear()
    print_summary(total_files_scanned, total_files_matched, total_matches)
