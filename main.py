#!/usr/bin/env python3
import re
import pyperclip


def max_backtick_run(text: str) -> int:
    """Return the length of the longest consecutive backtick sequence."""
    runs = re.findall(r"`+", text)
    return max((len(r) for r in runs), default=0)


def wrap_in_code_fence(text: str, language: str = "") -> str:
    """Wrap text in a code fence, using enough backticks to avoid conflicts."""
    fence = "`" * max(3, max_backtick_run(text) + 1)
    content = text.rstrip("\n")
    return f"\n{fence}{language}\n{content}\n{fence}\n"


def is_single_fenced_block(text: str) -> bool:
    """Return True if text is exactly one fenced code block."""
    lines = text.strip().splitlines()
    if len(lines) < 2:
        return False

    fence_pattern = re.compile(r"^(`{3,})(\w*)\s*$")
    opening_match = fence_pattern.match(lines[0])
    if not opening_match:
        return False

    opener = opening_match.group(1)
    # Closing fence must match or exceed opener length, with no language tag
    closing_match = re.match(rf"^`{{{len(opener)},}}$", lines[-1].strip())
    if not closing_match:
        return False

    # Ensure no other top-level fences in between
    for line in lines[1:-1]:
        if re.match(rf"^`{{{len(opener)},}}", line.lstrip()):
            return False

    return True


def add_code_block() -> None:
    """Wrap clipboard contents in a code fence."""
    try:
        content = pyperclip.paste()
    except pyperclip.PyperclipException as e:
        print(f"Clipboard error: {e}")
        return

    if not content.strip():
        return

    if is_single_fenced_block(content):
        return

    pyperclip.copy(wrap_in_code_fence(content))


if __name__ == "__main__":
    add_code_block()