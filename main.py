#!/usr/bin/env python3
import os
import re
import shutil
import subprocess
from urllib.parse import unquote, urlparse

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


def decode_file_uri(line: str) -> str | None:
    """Decode a single file:// URI to a plain path, or None if not one."""
    parsed = urlparse(line.strip())
    if parsed.scheme != "file" or not parsed.path:
        return None
    # Allow localhost as an authority (RFC 8089); reject remote hosts.
    if parsed.netloc not in ("", "localhost"):
        return None
    return unquote(parsed.path)


def decode_file_uris(text: str) -> str:
    """Convert file:// URIs to plain paths.

    Clipboard managers (e.g. Plasma/KDE) often expose copied files as
    newline-separated file:// URIs with percent-encoded characters. This
    strips the protocol header and decodes each URI back to a readable path.
    """
    lines = []
    for line in text.splitlines():
        decoded = decode_file_uri(line)
        lines.append(decoded if decoded is not None else line)
    return "\n".join(lines)


def copy_text(text: str) -> None:
    # Match Pyperclip's Wayland selection so reads and writes use the same backend.
    if (
        os.getenv("WAYLAND_DISPLAY")
        and shutil.which("wl-copy")
        and shutil.which("wl-paste")
    ):
        # MIME detection can mistake plain text for a binary file signature.
        subprocess.run(
            ["wl-copy", "--type", "text/plain;charset=utf-8"],
            input=text.encode("utf-8"),
            check=True,
        )
    else:
        pyperclip.copy(text)


def add_code_block() -> None:
    """Wrap clipboard contents in a code fence."""
    try:
        content = pyperclip.paste()
    except pyperclip.PyperclipException as e:
        print(f"Clipboard error: {e}")
        return

    if not content.strip():
        return

    original = content

    # Decode file:// URIs (Plasma/KDE expose copied files this way) before any
    # fence logic, so URIs are decoded even inside a pre-existing fence.
    content = decode_file_uris(content) if "file://" in content else content

    # Already a single fenced block: leave it to avoid double-wrapping, unless
    # the decode step above changed it (e.g. URIs inside a fence), in which
    # case write the decoded text back.
    if is_single_fenced_block(content):
        if content != original:
            copy_text(content)
        return

    copy_text(wrap_in_code_fence(content))


if __name__ == "__main__":
    add_code_block()