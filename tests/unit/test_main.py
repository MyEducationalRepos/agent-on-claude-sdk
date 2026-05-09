"""Unit tests for the CLI entrypoint."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from agent_on_claude_sdk.models import RunRecord, RunStatus


def _make_record(status: RunStatus) -> RunRecord:
    r = RunRecord(task="t", model="m")
    r.finish(status)
    return r


class TestMainArgParsing:
    def test_no_args_returns_1(self):
        from agent_on_claude_sdk.main import main
        assert main([]) == 1

    def test_task_joined_from_multiple_words(self):
        from agent_on_claude_sdk.main import main

        record = _make_record(RunStatus.complete)
        with (
            patch("agent_on_claude_sdk.main.load_settings", return_value=SimpleNamespace(
                anthropic_api_key="k", tavily_api_key="k2",
                model="claude-test", max_turns=5, max_result_chars=500,
            )),
            patch("agent_on_claude_sdk.main.run", return_value=record) as mock_run,
            patch("agent_on_claude_sdk.main.FsStore"),
            patch("agent_on_claude_sdk.main.Tracer"),
            patch("agent_on_claude_sdk.main._register_tools"),
        ):
            main(["hello", "world"])
            call_task = mock_run.call_args[0][0]
            assert call_task == "hello world"


class TestMainExitCodes:
    def _run_main(self, status: RunStatus):
        from agent_on_claude_sdk.main import main
        record = _make_record(status)
        with (
            patch("agent_on_claude_sdk.main.load_settings", return_value=SimpleNamespace(
                anthropic_api_key="k", tavily_api_key="k2",
                model="claude-test", max_turns=5, max_result_chars=500,
            )),
            patch("agent_on_claude_sdk.main.run", return_value=record),
            patch("agent_on_claude_sdk.main.FsStore"),
            patch("agent_on_claude_sdk.main.Tracer"),
            patch("agent_on_claude_sdk.main._register_tools"),
        ):
            return main(["task"])

    def test_complete_returns_0(self):
        assert self._run_main(RunStatus.complete) == 0

    def test_max_turns_returns_1(self):
        assert self._run_main(RunStatus.max_turns) == 1

    def test_error_returns_1(self):
        assert self._run_main(RunStatus.error) == 1


class TestMainConfigError:
    def test_missing_env_returns_2(self):
        from agent_on_claude_sdk.main import main
        with patch("agent_on_claude_sdk.main.load_settings", side_effect=RuntimeError("Missing ANTHROPIC_API_KEY")):
            assert main(["task"]) == 2


class TestRegisterTools:
    def test_registers_three_tools(self):
        import agent_on_claude_sdk.tools as registry
        from agent_on_claude_sdk.main import _register_tools
        registry.clear()
        _register_tools()
        names = {s["name"] for s in registry.schemas()}
        assert names == {"read_file", "write_file", "web_search"}
        registry.clear()
