# filesearch

A fast CLI tool to recursively search files for a word or phrase. Supports **PDF text extraction** and any plain-text file type (`.txt`, `.csv`, `.py`, `.log`, `.json`, etc.).

## Features

- Search inside **PDF files** (extracts text page by page)
- Search any **plain-text file type** by extension
- Search **all non-binary files** with `-t "*"`
- **Case-insensitive** matching with `-i`
- **Live progress spinner** while scanning
- **ANSI-colored** output with highlighted matches
- Control search depth with `--max-depth`

## Installation

### Option 1: pip install (requires Python 3.11+)

Install directly from GitHub:

```bash
pip install git+https://github.com/swamivr/filesearch.git
```

Or clone and install locally:

```bash
git clone https://github.com/swamivr/filesearch.git
cd filesearch
pip install .
```

### Option 2: Standalone executable (no Python required)

Download the pre-built binary for your platform from the
[Releases](https://github.com/swamivr/filesearch/releases) page:

| Platform | File |
|----------|------|
| Windows  | `filesearch-windows.exe` |
| macOS    | `filesearch-macos` |
| Linux    | `filesearch-linux` |

On macOS/Linux, make it executable after downloading:

```bash
chmod +x filesearch-macos    # or filesearch-linux
```

Optionally move it to a directory on your PATH:

```bash
# macOS / Linux
sudo mv filesearch-macos /usr/local/bin/filesearch

# Windows — move filesearch-windows.exe to a folder in your PATH
# or run it directly from the download location
```

## Usage

```
filesearch <search_term> [folder] [options]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `search_term` | The word or phrase to search for (use quotes for multi-word) |
| `folder` | Root folder to search (default: current directory) |

### Options

| Option | Description |
|--------|-------------|
| `-t TYPE` | File extension to filter by: `pdf`, `txt`, `csv`, `py`, `*` for all (default: `pdf`) |
| `-i` | Case-insensitive search |
| `--max-depth N` | Limit subfolder depth (0 = root only) |
| `-v` | Show version |
| `-h` | Show help |

### Examples

```bash
# Search PDFs in current directory
filesearch "invoice"

# Search Python files in ./src
filesearch "TODO" ./src -t py

# Case-insensitive search in log files
filesearch "error" /var/logs -t log -i

# Search all non-binary files
filesearch "import os" . -t "*"

# Limit search depth
filesearch "config" . -t yaml --max-depth 2
```

### Output

For each matching file, the full path is printed followed by every matching line:

- **PDF files** show the page number: `p.   1:`
- **Text files** show the line number: `   42:`

A summary of files scanned, matched, and total matches is printed at the end.

## License

MIT
