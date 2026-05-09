"""read_file tool — safely reads a local file and returns its content.

Path-safety rule: reads are restricted to the current working directory tree.
Any attempt to read outside that boundary returns an error string.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

SCHEMA: dict[str, Any] = {
    "name": "read_file",
    "description": (
        "Read the contents of a local file and return them as a string. "
        "Reads are restricted to the current working directory tree."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Relative or absolute path to the file to read.",
            }
        },
        "required": ["path"],
    },
}


def handler(tool_input: dict[str, Any]) -> str:
    """Read and return the file at *tool_input['path']*.

    Returns an error string (not a raised exception) so the model can react.
    """
    path = Path(tool_input["path"])
    try:
        resolved = path.resolve()
        cwd = Path.cwd().resolve()
        if not str(resolved).startswith(str(cwd)):
            return f"[error] Path outside working directory: {path}"
    except OSError as exc:
        return f"[error] Cannot resolve path {path}: {exc}"

    try:
        return resolved.read_text(encoding="utf-8")
    except FileNotFoundError:
        return f"[error] File not found: {path}"
    except PermissionError:
        return f"[error] Permission denied: {path}"
    except OSError as exc:
        return f"[error] Cannot read {path}: {exc}"
