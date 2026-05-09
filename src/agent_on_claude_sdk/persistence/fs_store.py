"""Filesystem-based run store — canonical MVP persistence layer."""

from __future__ import annotations

import json
from pathlib import Path

from agent_on_claude_sdk.models import RunRecord


class FsStore:
    """Reads and writes RunRecord metadata under a configurable root directory."""

    def __init__(self, root: Path | None = None) -> None:
        self._root = root or Path("runs")

    def _record_path(self, run_id: str) -> Path:
        return self._root / run_id / "record.json"

    def save(self, record: RunRecord) -> None:
        """Persist a RunRecord; creates the run directory if needed."""
        path = self._record_path(record.run_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(record.as_dict(), indent=2), encoding="utf-8")

    def load(self, run_id: str) -> RunRecord:
        """Load a RunRecord by run ID; raises FileNotFoundError if absent."""
        path = self._record_path(run_id)
        data = json.loads(path.read_text(encoding="utf-8"))
        from agent_on_claude_sdk.models import RunStatus

        record = RunRecord(
            task=data["task"],
            model=data["model"],
            run_id=data["run_id"],
        )
        record.status = RunStatus(data["status"])
        record.started_at = data["started_at"]
        record.ended_at = data.get("ended_at")
        record.turns_count = data.get("turns_count", 0)
        record.error_summary = data.get("error_summary")
        return record

    def run_dir(self, run_id: str) -> Path:
        """Return (and create) the directory for a run's artifacts and trace."""
        d = self._root / run_id
        d.mkdir(parents=True, exist_ok=True)
        return d

    def list_runs(self) -> list[str]:
        """Return run IDs for all persisted runs, sorted by name."""
        if not self._root.exists():
            return []
        return sorted(p.name for p in self._root.iterdir() if p.is_dir())
