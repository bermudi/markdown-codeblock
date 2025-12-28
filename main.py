#!/usr/bin/env python3
import pyperclip


def indent_nested_code_blocks(text: str, indent: str = "    ") -> str:
    """Indent fenced code blocks so they remain literal inside an outer fence."""
    lines = text.splitlines()
    trailing_newline = text.endswith("\n")

    indented_lines = []
    inside_fence = False
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```"):
            indented_lines.append(f"{indent}{line}")
            inside_fence = not inside_fence
            continue

        if inside_fence:
            indented_lines.append(f"{indent}{line}")
        else:
            indented_lines.append(line)

    result = "\n".join(indented_lines)
    if trailing_newline:
        result += "\n"

    return result


def has_outer_code_fence(text: str) -> bool:
    """Return True when text is already wrapped in a top-level ``` fence."""
    stripped = text.strip()
    return stripped.startswith("```") and stripped.endswith("```")


def add_code_block():
    """Wrap clipboard contents in a code fence while escaping inner fences."""
    clipboard_content = pyperclip.paste()
    if not isinstance(clipboard_content, str):
        clipboard_content = str(clipboard_content)

    if has_outer_code_fence(clipboard_content):
        # Avoid re-wrapping content that's already fenced (prevents recursion).
        pyperclip.copy(clipboard_content)
        return

    safe_content = indent_nested_code_blocks(clipboard_content)
    pyperclip.copy(f"\n```\n{safe_content}\n```\n")


if __name__ == "__main__":
    add_code_block()
