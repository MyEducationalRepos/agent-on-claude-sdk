"""Unit tests for shared runtime models."""

from agent_on_claude_sdk.models import RunRecord, RunStatus, ToolResult, TraceEvent


class TestRunStatus:
    def test_values(self):
        assert RunStatus.running.value == "running"
        assert RunStatus.complete.value == "complete"
        assert RunStatus.max_turns.value == "max_turns"
        assert RunStatus.error.value == "error"

    def test_is_str(self):
        assert isinstance(RunStatus.complete, str)


class TestToolResult:
    def test_defaults(self):
        r = ToolResult(tool_use_id="tu_1", content="ok")
        assert r.is_error is False

    def test_error_flag(self):
        r = ToolResult(tool_use_id="tu_2", content="fail", is_error=True)
        assert r.is_error is True


class TestTraceEvent:
    def test_as_dict_keys(self):
        ev = TraceEvent(event_type="turn_start", turn=1, content={"msg": "hi"})
        d = ev.as_dict()
        assert set(d) == {"event_type", "turn", "content", "timestamp"}
        assert d["event_type"] == "turn_start"
        assert d["turn"] == 1

    def test_timestamp_is_iso(self):
        ev = TraceEvent(event_type="done", turn=0, content=None)
        assert "T" in ev.timestamp  # ISO-8601 contains 'T'


class TestRunRecord:
    def test_defaults(self):
        r = RunRecord(task="say hello", model="claude-3-5-haiku-20241022")
        assert r.status == RunStatus.running
        assert r.ended_at is None
        assert r.turns_count == 0
        assert len(r.run_id) == 36  # UUID4 string length

    def test_finish_complete(self):
        r = RunRecord(task="t", model="m")
        r.finish(RunStatus.complete)
        assert r.status == RunStatus.complete
        assert r.ended_at is not None
        assert r.error_summary is None

    def test_finish_error(self):
        r = RunRecord(task="t", model="m")
        r.finish(RunStatus.error, error_summary="timeout")
        assert r.status == RunStatus.error
        assert r.error_summary == "timeout"

    def test_as_dict_keys(self):
        r = RunRecord(task="t", model="m")
        d = r.as_dict()
        expected = {
            "run_id",
            "task",
            "model",
            "status",
            "started_at",
            "ended_at",
            "turns_count",
            "error_summary",
        }
        assert set(d) == expected

    def test_as_dict_status_is_string(self):
        r = RunRecord(task="t", model="m")
        assert isinstance(r.as_dict()["status"], str)
