"""Integration tests: harness loop → FsStore persistence."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

import agent_on_claude_sdk.tools as tool_registry
from agent_on_claude_sdk.harness import run
from agent_on_claude_sdk.models import RunRecord, RunStatus
from agent_on_claude_sdk.persistence.fs_store import FsStore
from agent_on_claude_sdk.tracing import Tracer


@pytest.fixture(autouse=True)
def clean_registry():
    tool_registry.clear()
    yield
    tool_registry.clear()


def _settings(max_turns: int = 5):
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


class TestPersistence:
    def test_record_saved_on_complete(self, tmp_path: Path):
        store = FsStore(tmp_path / "runs")
        tracer = Tracer(tmp_path / "runs" / "test-run")
        record = RunRecord(task="hello", model="claude-test")

        client = MagicMock()
        client.messages.create.return_value = _end_turn_response()

        run(
            "hello",
            settings=_settings(),
            tracer=tracer,
            record=record,
            store=store,
            client=client,
        )

        loaded = store.load(record.run_id)
        assert loaded.status == RunStatus.complete
        assert loaded.task == "hello"

    def test_run_id_appears_in_list(self, tmp_path: Path):
        store = FsStore(tmp_path / "runs")
        tracer = Tracer(tmp_path / "runs" / "test-run")
        record = RunRecord(task="list-me", model="claude-test")

        client = MagicMock()
        client.messages.create.return_value = _end_turn_response()

        run(
            "list-me",
            settings=_settings(),
            tracer=tracer,
            record=record,
            store=store,
            client=client,
        )

        assert record.run_id in store.list_runs()

    def test_trace_file_written(self, tmp_path: Path):
        store = FsStore(tmp_path / "runs")
        record = RunRecord(task="trace-me", model="claude-test")
        tracer = Tracer(store.run_dir(record.run_id))

        client = MagicMock()
        client.messages.create.return_value = _end_turn_response()

        run(
            "trace-me",
            settings=_settings(),
            tracer=tracer,
            record=record,
            store=store,
            client=client,
        )

        trace_path = store.run_dir(record.run_id) / "trace.jsonl"
        assert trace_path.exists()
        lines = trace_path.read_text().strip().splitlines()
        assert len(lines) >= 1

    def test_initial_save_before_loop(self, tmp_path: Path):
        """store.save called at least twice: once at start, once at finish."""
        store = FsStore(tmp_path / "runs")
        tracer = Tracer(tmp_path / "runs" / "test-run")
        record = RunRecord(task="init-save", model="claude-test")

        save_calls: list[str] = []
        original_save = store.save

        def recording_save(r: RunRecord) -> None:
            save_calls.append(r.status.value)
            original_save(r)

        store.save = recording_save  # type: ignore[method-assign]

        client = MagicMock()
        client.messages.create.return_value = _end_turn_response()

        run(
            "init-save",
            settings=_settings(),
            tracer=tracer,
            record=record,
            store=store,
            client=client,
        )

        assert len(save_calls) >= 2
        assert save_calls[0] == "running"
        assert save_calls[-1] == "complete"

    def test_error_status_persisted(self, tmp_path: Path):
        store = FsStore(tmp_path / "runs")
        tracer = Tracer(tmp_path / "runs" / "test-run")
        record = RunRecord(task="bad", model="claude-test")

        resp = MagicMock()
        resp.stop_reason = "unknown_reason"
        resp.content = []
        client = MagicMock()
        client.messages.create.return_value = resp

        run(
            "bad",
            settings=_settings(),
            tracer=tracer,
            record=record,
            store=store,
            client=client,
        )

        loaded = store.load(record.run_id)
        assert loaded.status == RunStatus.error
