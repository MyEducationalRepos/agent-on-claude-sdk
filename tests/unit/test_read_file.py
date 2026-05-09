"""Unit tests for the read_file tool."""

from pathlib import Path

import pytest

from agent_on_claude_sdk.tools.read_file import SCHEMA, handler


@pytest.fixture()
def cwd_tmp(tmp_path, monkeypatch):
    """Change cwd into tmp_path so handler's boundary check passes."""
    monkeypatch.chdir(tmp_path)
    return tmp_path


class TestSchema:
    def test_name(self):
        assert SCHEMA["name"] == "read_file"

    def test_required_path(self):
        assert "path" in SCHEMA["input_schema"]["required"]


class TestHandler:
    def test_reads_existing_file(self, cwd_tmp: Path):
        f = cwd_tmp / "hello.txt"
        f.write_text("hello world", encoding="utf-8")
        result = handler({"path": str(f)})
        assert result == "hello world"

    def test_missing_file_returns_error_string(self, cwd_tmp: Path):
        result = handler({"path": str(cwd_tmp / "nope.txt")})
        assert result.startswith("[error]")
        assert "not found" in result.lower()

    def test_empty_file_returns_empty_string(self, cwd_tmp: Path):
        f = cwd_tmp / "empty.txt"
        f.write_text("", encoding="utf-8")
        assert handler({"path": str(f)}) == ""

    def test_multiline_content_preserved(self, cwd_tmp: Path):
        content = "line1\nline2\nline3"
        f = cwd_tmp / "multi.txt"
        f.write_text(content, encoding="utf-8")
        assert handler({"path": str(f)}) == content

    def test_returns_string(self, cwd_tmp: Path):
        f = cwd_tmp / "t.txt"
        f.write_text("x", encoding="utf-8")
        assert isinstance(handler({"path": str(f)}), str)

    def test_path_traversal_blocked(self, cwd_tmp: Path, tmp_path: Path):
        """Absolute path outside cwd must be rejected."""
        outside = tmp_path.parent / "outside_secret.txt"
        outside.write_text("secret", encoding="utf-8")
        result = handler({"path": str(outside)})
        assert result.startswith("[error]")
        assert "outside working directory" in result
        if outside.exists():
            outside.unlink()
