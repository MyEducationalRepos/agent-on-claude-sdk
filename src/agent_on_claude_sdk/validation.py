"""Post-write formatting hook — runs ruff format on Python files."""

from __future__ import annotations

import subprocess
from pathlib import Path


def format_if_python(path: str | Path) -> bool:
    """Run ``ruff format`` on *path* if it is a Python file.

    Args:
        path: Path to the file that was just written.

    Returns:
        ``True`` if formatting was attempted (file is ``.py``), ``False`` otherwise.

    The function never raises; formatting errors are swallowed so a missing or
    broken ``ruff`` binary cannot crash the agent runtime.
    """
    p = Path(path)
    if p.suffix != ".py":
        return False
    try:
        subprocess.run(
            ["ruff", "format", str(p)],
            check=False,
            capture_output=True,
        )
    except FileNotFoundError:
        # ruff not on PATH — silently skip
        pass
    return True
