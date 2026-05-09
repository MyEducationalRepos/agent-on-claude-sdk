"""Tests for visible console progress output from the harness."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

import agent_on_claude_sdk.tools as tool_registry
from agent_on_claude_sdk.harness import run
from agent_on_claude_sdk.models import RunRecord
from agent_on_claude_sdk.tracing import Tracer


@pytest.fixture(autouse=True)
def clean_registry():
    tool_registry.clear()
    yield
    tool_registry.clear()


def _settings():
    return SimpleNamespace(
        anthropic_api_key="sk-ant-test",
        model="claude-test",
        max_turns=5,
        max_result_chars=500,
    )


def _end_turn():
    r = MagicMock()
    r.stop_reason = "end_turn"
    r.content = []
    return r


def _tool_use(name: str, tool_id: str = "tu_1"):
    from types import SimpleNamespace as SN

    block = SN(type="tool_use", name=name, input={}, id=tool_id)
    r = MagicMock()
    r.stop_reason = "tool_use"
    r.content = [block]
    return r


def _tracer(tmp_path: Path) -> Tracer:
    return Tracer(tmp_path / "run")


class TestProgressOutput:
    def test_run_header_printed(self, tmp_path, capsys):
        client = MagicMock()
        client.messages.create.return_value = _end_turn()
        run(
            "task",
            settings=_settings(),
            tracer=_tracer(tmp_path),
            record=RunRecord(task="task", model="m"),
            client=client,
        )
        out = capsys.readouterr().out
        assert "[run]" in out
        assert "claude-test" in out

    def test_turn_progress_printed(self, tmp_path, capsys):
        client = MagicMock()
        client.messages.create.return_value = _end_turn()
        run(
            "task",
            settings=_settings(),
            tracer=_tracer(tmp_path),
            record=RunRecord(task="task", model="m"),
            client=client,
        )
        out = capsys.readouterr().out
        assert "[turn 1/" in out
        assert "thinking" in out

    def test_done_complete_printed(self, tmp_path, capsys):
        client = MagicMock()
        client.messages.create.return_value = _end_turn()
        run(
            "task",
            settings=_settings(),
            tracer=_tracer(tmp_path),
            record=RunRecord(task="task", model="m"),
            client=client,
        )
        out = capsys.readouterr().out
        assert "[done]" in out
        assert "complete" in out

    def test_tool_name_printed(self, tmp_path, capsys):
        tool_registry.register(
            {
                "name": "ping",
                "description": "",
                "input_schema": {"type": "object", "properties": {}, "required": []},
            },
            lambda _: "pong",
        )
        client = MagicMock()
        client.messages.create.side_effect = [_tool_use("ping"), _end_turn()]
        run(
            "task",
            settings=_settings(),
            tracer=_tracer(tmp_path),
            record=RunRecord(task="task", model="m"),
            client=client,
        )
        out = capsys.readouterr().out
        assert "[tool] ping" in out

    def test_done_max_turns_printed(self, tmp_path, capsys):
        tool_registry.register(
            {
                "name": "loop",
                "description": "",
                "input_schema": {"type": "object", "properties": {}, "required": []},
            },
            lambda _: "ok",
        )
        client = MagicMock()
        client.messages.create.return_value = _tool_use("loop")
        run(
            "task",
            settings=_settings(),
            tracer=_tracer(tmp_path),
            record=RunRecord(task="task", model="m"),
            client=client,
        )
        out = capsys.readouterr().out
        assert "max_turns" in out

    def test_done_error_printed(self, tmp_path, capsys):
        r = MagicMock()
        r.stop_reason = "weird_stop"
        r.content = []
        client = MagicMock()
        client.messages.create.return_value = r
        run(
            "task",
            settings=_settings(),
            tracer=_tracer(tmp_path),
            record=RunRecord(task="task", model="m"),
            client=client,
        )
        out = capsys.readouterr().out
        assert "error" in out
