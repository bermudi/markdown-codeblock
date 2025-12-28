
# markdown-codeblock

Small clipboard helper that wraps any selected text in a Markdown code fence while safely handling nested fences. Designed for quickly pasting into LLM chats without breaking formatting.

## Features

1. **Clipboard aware:** Pulls the active clipboard contents via `pyperclip`.
2. **Nested code block safety:** Detects existing ``` fences and indents their contents so the outer wrapper remains intact.
3. **Idempotent:** If your clipboard already contains a fenced block, the script leaves it untouched to avoid double-wrapping.

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

The script will:

- Skip wrapping if the clipboard already starts/ends with ``` to prevent recursion.
- Indent inner fences so they stay literal.
- Wrap the final text in a clean fence with blank lines around it for readability.

## Customization

- **Indent width:** Adjust the default indentation (`indent_nested_code_blocks(indent="    ")`) if you prefer tabs or another width.
- **Hotkeys:** Map your window manager/terminal launcher to run `uv run python main.py` directly for faster access.

## Troubleshooting

- *Clipboard empty or non-text:* Pyperclip exposes only the text clipboard. If nothing happens, ensure the clipboard has text and that your OS clipboard back-end is supported.
- *Permission errors on Linux:* Install `xclip` or `xsel` (Pyperclip requirements) if you’re on X11. For Wayland, ensure the appropriate compatibility layer is available.

## License

MIT (see `LICENSE` if provided, or update this section with your preferred license).
