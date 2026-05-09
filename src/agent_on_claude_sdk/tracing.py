"""Structured, append-only trace writer for agent runs."""

from __future__ import annotations

import json
from pathlib import Path

from agent_on_claude_sdk.models import TraceEvent


class Tracer:
    """Writes TraceEvent records as newline-delimited JSON to a trace file."""

    def __init__(self, run_dir: Path) -> None:
        self._path = run_dir / "trace.jsonl"
        run_dir.mkdir(parents=True, exist_ok=True)

    def emit(self, event: TraceEvent) -> None:
        """Append one event to the trace file (never overwrites)."""
        with self._path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(event.as_dict()) + "\n")

    def events(self) -> list[dict]:
        """Return all recorded events (for testing / inspection)."""
        if not self._path.exists():
            return []
        return [
            json.loads(line)
            for line in self._path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
