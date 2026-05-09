"""Unit tests for the filesystem run store."""

from pathlib import Path

import pytest

from agent_on_claude_sdk.models import RunRecord, RunStatus
from agent_on_claude_sdk.persistence.fs_store import FsStore


@pytest.fixture()
def store(tmp_path: Path) -> FsStore:
    return FsStore(root=tmp_path / "runs")


class TestFsStoreSave:
    def test_creates_record_file(self, store: FsStore, tmp_path: Path):
        r = RunRecord(task="t", model="m")
        store.save(r)
        assert (tmp_path / "runs" / r.run_id / "record.json").exists()

    def test_record_is_valid_json(self, store: FsStore, tmp_path: Path):
        import json

        r = RunRecord(task="hello", model="claude-x")
        store.save(r)
        raw = (tmp_path / "runs" / r.run_id / "record.json").read_text()
        data = json.loads(raw)
        assert data["task"] == "hello"

    def test_overwrite_on_second_save(self, store: FsStore):
        r = RunRecord(task="t", model="m")
        store.save(r)
        r.finish(RunStatus.complete)
        store.save(r)
        loaded = store.load(r.run_id)
        assert loaded.status == RunStatus.complete


class TestFsStoreLoad:
    def test_roundtrip(self, store: FsStore):
        r = RunRecord(task="my task", model="claude-3")
        r.finish(RunStatus.max_turns)
        store.save(r)
        loaded = store.load(r.run_id)
        assert loaded.run_id == r.run_id
        assert loaded.task == "my task"
        assert loaded.status == RunStatus.max_turns
        assert loaded.ended_at == r.ended_at

    def test_missing_raises(self, store: FsStore):
        with pytest.raises(FileNotFoundError):
            store.load("does-not-exist")


class TestFsStoreRunDir:
    def test_creates_directory(self, store: FsStore, tmp_path: Path):
        d = store.run_dir("run-abc")
        assert d.is_dir()
        assert d == tmp_path / "runs" / "run-abc"


class TestFsStoreListRuns:
    def test_empty_when_no_root(self, tmp_path: Path):
        store = FsStore(root=tmp_path / "nonexistent")
        assert store.list_runs() == []

    def test_lists_saved_runs(self, store: FsStore):
        r1 = RunRecord(task="a", model="m")
        r2 = RunRecord(task="b", model="m")
        store.save(r1)
        store.save(r2)
        ids = store.list_runs()
        assert r1.run_id in ids
        assert r2.run_id in ids
