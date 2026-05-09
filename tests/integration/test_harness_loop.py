"""Integration tests: full harness loop with mocked Anthropic client."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import agent_on_claude_sdk.tools as tool_registry
from agent_on_claude_sdk.harness import run
from agent_on_claude_sdk.models import RunRecord, RunStatus
from agent_on_claude_sdk.persistence.fs_store import FsStore
from agent_on_claude_sdk.tracing import Tracer


# ── helpers ───────────────────────────────────────────────────────────────────


def _settings(max_turns: int = 3):
    return SimpleNamespace(
        anthropic_api_key="sk-ant-test",
        model="claude-test",
        max_turns=max_turns,
        max_result_chars=500,
    )


def _end_turn_response():
    resp = MagicMock()
    resp.stop_reason = "end_turn"
    resp.content = []
    return resp


def _tool_use_then_end_turn(tool_name: str, tool_id: str, tool_input: dict):
    """Return two responses: first a tool_use, then end_turn."""
    tool_block = MagicMock()
    tool_block.type = "tool_use"
    tool_block.id = tool_id
    tool_block.name = tool_name
    tool_block.input = tool_input

    turn1 = MagicMock()
    turn1.stop_reason = "tool_use"
    turn1.content = [tool_block]

    turn2 = _end_turn_response()
    return [turn1, turn2]


# ── tests ─────────────────────────────────────────────────────────────────────


class TestHarnessLoop:
    def setup_method(self):
        tool_registry.clear()

    def teardown_method(self):
        tool_registry.clear()

    def test_complete_on_end_turn(self, tmp_path: Path):
        record = RunRecord(task="hello", model="claude-test")
        tracer = Tracer(tmp_path / record.run_id)
        client = MagicMock()
        client.messages.create.return_value = _end_turn_response()

        result = run("hello", _settings(), tracer, record, client=client)

        assert result.status == RunStatus.complete
        assert result.turns_count == 1

    def test_max_turns_exhausted(self, tmp_path: Path):
        record = RunRecord(task="loop", model="claude-test")
        tracer = Tracer(tmp_path / record.run_id)

        # Every response is tool_use with no registered tool → dispatches error,
        # loop continues until max_turns.
        tool_block = MagicMock()
        tool_block.type = "tool_use"
        tool_block.id = "tu-1"
        tool_block.name = "unknown_tool"
        tool_block.input = {}

        resp = MagicMock()
        resp.stop_reason = "tool_use"
        resp.content = [tool_block]

        client = MagicMock()
        client.messages.create.return_value = resp

        result = run("loop", _settings(max_turns=2), tracer, record, client=client)

        assert result.status == RunStatus.max_turns
        assert result.turns_count == 2

    def test_tool_use_dispatched_then_complete(self, tmp_path: Path):
        """A registered tool is called and the loop completes on the next turn."""
        calls: list[dict] = []

        def echo_handler(input: dict) -> str:  # noqa: A002
            calls.append(input)
            return "pong"

        tool_registry.register(
            {
                "name": "echo",
                "description": "echo",
                "input_schema": {"type": "object", "properties": {}, "required": []},
            },
            echo_handler,
        )

        responses = iter(_tool_use_then_end_turn("echo", "tu-echo-1", {"msg": "ping"}))
        client = MagicMock()
        client.messages.create.side_effect = lambda **_: next(responses)

        record = RunRecord(task="echo test", model="claude-test")
        tracer = Tracer(tmp_path / record.run_id)

        result = run("echo test", _settings(), tracer, record, client=client)

        assert result.status == RunStatus.complete
        assert calls == [{"msg": "ping"}]

    def test_store_persists_complete(self, tmp_path: Path):
        store = FsStore(tmp_path / "runs")
        record = RunRecord(task="persist", model="claude-test")
        tracer = Tracer(store.run_dir(record.run_id))
        client = MagicMock()
        client.messages.create.return_value = _end_turn_response()

        run("persist", _settings(), tracer, record, store=store, client=client)

        loaded = store.load(record.run_id)
        assert loaded.status == RunStatus.complete

    def test_trace_events_written(self, tmp_path: Path):
        store = FsStore(tmp_path / "runs")
        record = RunRecord(task="trace", model="claude-test")
        tracer = Tracer(store.run_dir(record.run_id))
        client = MagicMock()
        client.messages.create.return_value = _end_turn_response()

        run("trace", _settings(), tracer, record, store=store, client=client)

        trace_path = store.run_dir(record.run_id) / "trace.jsonl"
        assert trace_path.exists()
        lines = trace_path.read_text().strip().splitlines()
        # Expect at least: run_start, turn_start, turn_end, done
        assert len(lines) >= 4

    def test_error_on_unknown_stop_reason(self, tmp_path: Path):
        record = RunRecord(task="bad", model="claude-test")
        tracer = Tracer(tmp_path / record.run_id)

        resp = MagicMock()
        resp.stop_reason = "totally_unknown"
        resp.content = []
        client = MagicMock()
        client.messages.create.return_value = resp

        result = run("bad", _settings(), tracer, record, client=client)

        assert result.status == RunStatus.error
        assert "totally_unknown" in (result.error_summary or "")
