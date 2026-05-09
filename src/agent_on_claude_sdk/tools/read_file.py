"""read_file tool — safely reads a local file and returns its content."""

from __future__ import annotations

from pathlib import Path
from typing import Any

SCHEMA: dict[str, Any] = {
    "name": "read_file",
    "description": "Read the contents of a local file and return them as a string.",
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
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return f"[error] File not found: {path}"
    except PermissionError:
        return f"[error] Permission denied: {path}"
    except OSError as exc:
        return f"[error] Cannot read {path}: {exc}"
