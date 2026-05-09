"""Shared typed contracts for tool results, trace events, and run records."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class RunStatus(str, Enum):
    running = "running"
    complete = "complete"
    max_turns = "max_turns"
    error = "error"


@dataclass
class ToolResult:
    """Structured output returned by a tool dispatcher."""

    tool_use_id: str
    content: str
    is_error: bool = False


@dataclass
class TraceEvent:
    """One append-only entry written to runs/<run-id>/trace.jsonl."""

    event_type: str  # e.g. "turn_start", "tool_call", "tool_result", "done"
    turn: int
    content: Any
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def as_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "turn": self.turn,
            "content": self.content,
            "timestamp": self.timestamp,
        }


@dataclass
class RunRecord:
    """Persistent metadata for a single agent run."""

    task: str
    model: str
    run_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: RunStatus = RunStatus.running
    started_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    ended_at: str | None = None
    turns_count: int = 0
    error_summary: str | None = None

    def finish(self, status: RunStatus, error_summary: str | None = None) -> None:
        self.status = status
        self.ended_at = datetime.now(timezone.utc).isoformat()
        self.error_summary = error_summary

    def as_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "task": self.task,
            "model": self.model,
            "status": self.status.value,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "turns_count": self.turns_count,
            "error_summary": self.error_summary,
        }
