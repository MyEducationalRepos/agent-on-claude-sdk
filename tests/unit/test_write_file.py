"""Unit tests for the write_file tool."""

from pathlib import Path

import pytest

from agent_on_claude_sdk.tools.write_file import SCHEMA, handler


class TestSchema:
    def test_name(self):
        assert SCHEMA["name"] == "write_file"

    def test_required_fields(self):
        required = SCHEMA["input_schema"]["required"]
        assert "path" in required
        assert "content" in required


class TestHandler:
    def test_writes_file(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.chdir(tmp_path)
        result = handler({"path": "out.txt", "content": "hello"})
        assert (tmp_path / "out.txt").read_text() == "hello"
        assert "5" in result  # 5 characters

    def test_creates_parent_dirs(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.chdir(tmp_path)
        handler({"path": "a/b/c.txt", "content": "deep"})
        assert (tmp_path / "a" / "b" / "c.txt").exists()

    def test_overwrites_existing(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "f.txt").write_text("old")
        handler({"path": "f.txt", "content": "new"})
        assert (tmp_path / "f.txt").read_text() == "new"

    def test_returns_string(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.chdir(tmp_path)
        result = handler({"path": "r.txt", "content": "x"})
        assert isinstance(result, str)

    def test_path_traversal_rejected(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        monkeypatch.chdir(tmp_path)
        result = handler({"path": "../../etc/passwd", "content": "bad"})
        assert result.startswith("[error]")
        assert "outside" in result.lower()

    def test_absolute_path_inside_cwd_allowed(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        monkeypatch.chdir(tmp_path)
        abs_path = str(tmp_path / "ok.txt")
        result = handler({"path": abs_path, "content": "safe"})
        assert not result.startswith("[error]")
        assert (tmp_path / "ok.txt").read_text() == "safe"

    def test_absolute_path_outside_cwd_rejected(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        monkeypatch.chdir(tmp_path)
        result = handler({"path": "/tmp/injected.txt", "content": "bad"})
        assert result.startswith("[error]")
