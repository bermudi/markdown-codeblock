
# markdown-codeblock

Small clipboard helper that wraps any selected text in a Markdown code fence while safely handling nested fences. Designed for quickly pasting into LLM chats without breaking formatting.

## Features

1. **Clipboard aware:** Pulls the active clipboard contents via `pyperclip`.
2. **Nested code block safety:** Detects the longest run of backticks in the content and uses a longer fence (at least three backticks) so any inner fences stay literal.
3. **Idempotent:** If your clipboard already contains a fenced block, the script leaves it untouched to avoid double-wrapping.
4. **`file://` URI decoding:** When the clipboard contains `file://` URIs — as produced by KDE/Plasma and other file managers when you copy one or more files — the protocol header is stripped and percent-encoding is decoded into readable paths before wrapping.

## Requirements

- Python 3.12+
- [`uv`](https://github.com/astral-sh/uv) for dependency management (preferred in this repo)

Dependencies are listed in `pyproject.toml` and currently include:

- `pyperclip`

## Setup

```bash
# 1. Install uv if needed (see uv docs)
# 2. Sync dependencies and create the virtual environment
uv sync
```

This will create `.venv/` managed by uv and install `pyperclip`.

## Usage

1. Copy any text (from code, docs, etc.) to your clipboard.
2. Run the helper:

```bash
uv run python main.py
```

3. Paste the results into your LLM chat or Markdown document.

### Example: copied files

Selecting multiple files in Dolphin (or another KDE/Plasma file manager) and copying them puts `file://` URIs on the clipboard. Running the helper turns this:

```
file:///home/daniel/Downloads/SCOTUS%20Doubles%20Down%20-%20youtube.com.md
file:///home/daniel/Downloads/Lawfare%20Live%20June%2026%20-%20youtube.com.md
```

into:

```
/home/daniel/Downloads/SCOTUS Doubles Down - youtube.com.md
/home/daniel/Downloads/Lawfare Live June 26 - youtube.com.md
```

The same decoding applies to a single copied file. Content with no `file://` URIs is left untouched.

The script will:

- Skip wrapping if the clipboard already contains a single fenced block, to avoid double-wrapping.
- If `file://` URIs are present, strip the protocol header and percent-decode each line into a plain path (supports the `file://localhost/` form; remote hosts like `file://nas/...` are left untouched).
- Use a backtick fence long enough to enclose any backticks already in the content.
- Wrap the final text in a clean fence with blank lines around it for readability.

## Customization

- **Hotkeys:** Map your window manager/terminal launcher to run `uv run python main.py` directly for faster access.

## Troubleshooting

- *Clipboard empty or non-text:* Pyperclip exposes only the text clipboard. If nothing happens, ensure the clipboard has text and that your OS clipboard back-end is supported.
- *Permission errors on Linux:* Install `xclip` or `xsel` (Pyperclip requirements) if you’re on X11. For Wayland, ensure the appropriate compatibility layer is available.

## License

MIT (see `LICENSE` if provided, or update this section with your preferred license).
