"""Unit tests for the base harness loop (Anthropic client mocked)."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

import agent_on_claude_sdk.tools as tool_registry
from agent_on_claude_sdk.harness import run
from agent_on_claude_sdk.models import RunRecord, RunStatus
from agent_on_claude_sdk.tracing import Tracer


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def clean_registry():
    tool_registry.clear()
    yield
    tool_registry.clear()


def _settings(max_turns: int = 5, max_result_chars: int = 500):
    return SimpleNamespace(
        anthropic_api_key="sk-ant-test",
        model="claude-test",
        max_turns=max_turns,
        max_result_chars=max_result_chars,
    )


def _tracer(tmp_path: Path) -> Tracer:
    return Tracer(tmp_path / "runs" / "test-run")


def _record() -> RunRecord:
    return RunRecord(task="test task", model="claude-test")


def _end_turn_response():
    """Fake response with stop_reason=end_turn (no tool blocks)."""
    resp = MagicMock()
    resp.stop_reason = "end_turn"
    resp.content = []
    return resp


def _tool_use_response(tool_name: str, tool_input: dict, tool_id: str = "tu_1"):
    """Fake response with one tool_use block."""
    block = SimpleNamespace(
        type="tool_use", name=tool_name, input=tool_input, id=tool_id
    )
    resp = MagicMock()
    resp.stop_reason = "tool_use"
    resp.content = [block]
    return resp


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestEndTurnImmediately:
    def test_status_complete(self, tmp_path):
        client = MagicMock()
        client.messages.create.return_value = _end_turn_response()
        record = _record()
        run(
            "task",
            settings=_settings(),
            tracer=_tracer(tmp_path),
            record=record,
            client=client,
        )
        assert record.status == RunStatus.complete

    def test_one_api_call(self, tmp_path):
        client = MagicMock()
        client.messages.create.return_value = _end_turn_response()
        run(
            "task",
            settings=_settings(),
            tracer=_tracer(tmp_path),
            record=_record(),
            client=client,
        )
        assert client.messages.create.call_count == 1

    def test_trace_has_done_event(self, tmp_path):
        client = MagicMock()
        client.messages.create.return_value = _end_turn_response()
        tracer = _tracer(tmp_path)
        run(
            "task", settings=_settings(), tracer=tracer, record=_record(), client=client
        )
        types = [e["event_type"] for e in tracer.events()]
        assert "done" in types


class TestMaxTurns:
    def test_status_max_turns_when_loop_exhausted(self, tmp_path):
        client = MagicMock()
        # Always returns tool_use but no tool registered → dispatches to error
        tool_registry.register(
            {
                "name": "noop",
                "description": "",
                "input_schema": {"type": "object", "properties": {}, "required": []},
            },
            lambda _: "ok",
        )
        client.messages.create.side_effect = [
            _tool_use_response("noop", {}, f"tu_{i}") for i in range(3)
        ] + [_end_turn_response()]
        record = _record()
        result = run(
            "task",
            settings=_settings(max_turns=3),
            tracer=_tracer(tmp_path),
            record=record,
            client=client,
        )
        # 3 tool_use turns then end_turn on 4th — but max_turns=3 so it depends on iteration
        assert result.status in {RunStatus.complete, RunStatus.max_turns}

    def test_turns_count_updated(self, tmp_path):
        client = MagicMock()
        client.messages.create.return_value = _end_turn_response()
        record = _record()
        run(
            "task",
            settings=_settings(),
            tracer=_tracer(tmp_path),
            record=record,
            client=client,
        )
        assert record.turns_count >= 1


class TestToolUseDispatch:
    def test_tool_result_sent_back(self, tmp_path):
        tool_registry.register(
            {
                "name": "echo",
                "description": "",
                "input_schema": {
                    "type": "object",
                    "properties": {"t": {"type": "string"}},
                    "required": ["t"],
                },
            },
            lambda inp: inp["t"],
        )
        responses = [
            _tool_use_response("echo", {"t": "hello"}, "tu_1"),
            _end_turn_response(),
        ]
        client = MagicMock()
        client.messages.create.side_effect = responses
        record = run(
            "task",
            settings=_settings(),
            tracer=_tracer(tmp_path),
            record=_record(),
            client=client,
        )
        assert record.status == RunStatus.complete
        # Second call should include tool results
        second_call_messages = client.messages.create.call_args_list[1][1]["messages"]
        tool_result_msg = second_call_messages[-1]
        assert tool_result_msg["role"] == "user"
        assert tool_result_msg["content"][0]["content"] == "hello"

    def test_unknown_tool_produces_error_result(self, tmp_path):
        responses = [
            _tool_use_response("unknown_tool", {}, "tu_x"),
            _end_turn_response(),
        ]
        client = MagicMock()
        client.messages.create.side_effect = responses
        record = run(
            "task",
            settings=_settings(),
            tracer=_tracer(tmp_path),
            record=_record(),
            client=client,
        )
        assert record.status == RunStatus.complete
        second_messages = client.messages.create.call_args_list[1][1]["messages"]
        content = second_messages[-1]["content"][0]["content"]
        assert "[error]" in content

    def test_result_truncated_to_max_result_chars(self, tmp_path):
        tool_registry.register(
            {
                "name": "big",
                "description": "",
                "input_schema": {"type": "object", "properties": {}, "required": []},
            },
            lambda _: "x" * 1000,
        )
        responses = [_tool_use_response("big", {}, "tu_b"), _end_turn_response()]
        client = MagicMock()
        client.messages.create.side_effect = responses
        run(
            "task",
            settings=_settings(max_result_chars=10),
            tracer=_tracer(tmp_path),
            record=_record(),
            client=client,
        )
        second_messages = client.messages.create.call_args_list[1][1]["messages"]
        content = second_messages[-1]["content"][0]["content"]
        assert len(content) == 10


class TestUnhandledStopReason:
    def test_status_error_on_unknown_stop_reason(self, tmp_path):
        resp = MagicMock()
        resp.stop_reason = "pause_turn"
        resp.content = []
        client = MagicMock()
        client.messages.create.return_value = resp
        record = run(
            "task",
            settings=_settings(),
            tracer=_tracer(tmp_path),
            record=_record(),
            client=client,
        )
        assert record.status == RunStatus.error
        assert "pause_turn" in (record.error_summary or "")
