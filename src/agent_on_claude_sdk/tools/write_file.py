"""write_file tool — safely writes content to a local file.

Path-safety rule: writes are restricted to the current working directory tree.
Any attempt to write outside that boundary returns an error string.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

SCHEMA: dict[str, Any] = {
    "name": "write_file",
    "description": (
        "Write text content to a local file. "
        "The file is created (including parent directories) if it does not exist. "
        "Writes are restricted to the current working directory tree."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Relative or absolute path for the file to write.",
            },
            "content": {
                "type": "string",
                "description": "Text content to write to the file.",
            },
        },
        "required": ["path", "content"],
    },
}


def handler(tool_input: dict[str, Any]) -> str:
    """Write *tool_input['content']* to *tool_input['path']*.

    Returns a success string or an ``[error]`` string — never raises.
    """
    target = Path(tool_input["path"])
    content: str = tool_input["content"]

    # Resolve against cwd to normalise relative paths and catch traversals.
    try:
        resolved = target.resolve()
        cwd = Path.cwd().resolve()
        if not str(resolved).startswith(str(cwd)):
            return f"[error] Path outside working directory: {target}"
    except OSError as exc:
        return f"[error] Cannot resolve path {target}: {exc}"

    try:
        resolved.parent.mkdir(parents=True, exist_ok=True)
        resolved.write_text(content, encoding="utf-8")
        return f"Written {len(content)} characters to {resolved}"
    except PermissionError:
        return f"[error] Permission denied: {resolved}"
    except OSError as exc:
        return f"[error] Cannot write {resolved}: {exc}"
