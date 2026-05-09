"""Unit tests for structured tracing."""

import json
from pathlib import Path

import pytest

from agent_on_claude_sdk.models import TraceEvent
from agent_on_claude_sdk.tracing import Tracer


@pytest.fixture()
def tracer(tmp_path: Path) -> Tracer:
    return Tracer(tmp_path / "runs" / "test-run")


class TestTracerEmit:
    def test_creates_file(self, tracer: Tracer, tmp_path: Path):
        tracer.emit(TraceEvent(event_type="turn_start", turn=1, content={}))
        trace_file = tmp_path / "runs" / "test-run" / "trace.jsonl"
        assert trace_file.exists()

    def test_appends_not_overwrites(self, tracer: Tracer):
        tracer.emit(TraceEvent(event_type="turn_start", turn=1, content={}))
        tracer.emit(TraceEvent(event_type="tool_call", turn=1, content={"name": "x"}))
        lines = tracer.events()
        assert len(lines) == 2

    def test_event_structure(self, tracer: Tracer):
        tracer.emit(TraceEvent(event_type="done", turn=3, content="end"))
        ev = tracer.events()[0]
        assert ev["event_type"] == "done"
        assert ev["turn"] == 3
        assert ev["content"] == "end"
        assert "timestamp" in ev

    def test_each_line_is_valid_json(self, tracer: Tracer, tmp_path: Path):
        tracer.emit(TraceEvent(event_type="a", turn=0, content=None))
        tracer.emit(TraceEvent(event_type="b", turn=1, content={"k": "v"}))
        raw = (tmp_path / "runs" / "test-run" / "trace.jsonl").read_text()
        for line in raw.splitlines():
            json.loads(line)  # must not raise


class TestTracerEvents:
    def test_empty_before_any_emit(self, tmp_path: Path):
        tracer = Tracer(tmp_path / "empty-run")
        assert tracer.events() == []

    def test_order_preserved(self, tracer: Tracer):
        types = ["turn_start", "tool_call", "tool_result", "done"]
        for i, t in enumerate(types):
            tracer.emit(TraceEvent(event_type=t, turn=i, content=None))
        evs = tracer.events()
        assert [e["event_type"] for e in evs] == types
