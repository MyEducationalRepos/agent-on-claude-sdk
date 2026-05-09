"""Unit tests for the read_file tool."""

from pathlib import Path

import pytest

from agent_on_claude_sdk.tools.read_file import SCHEMA, handler


class TestSchema:
    def test_name(self):
        assert SCHEMA["name"] == "read_file"

    def test_required_path(self):
        assert "path" in SCHEMA["input_schema"]["required"]


class TestHandler:
    def test_reads_existing_file(self, tmp_path: Path):
        f = tmp_path / "hello.txt"
        f.write_text("hello world", encoding="utf-8")
        result = handler({"path": str(f)})
        assert result == "hello world"

    def test_missing_file_returns_error_string(self, tmp_path: Path):
        result = handler({"path": str(tmp_path / "nope.txt")})
        assert result.startswith("[error]")
        assert "not found" in result.lower()

    def test_empty_file_returns_empty_string(self, tmp_path: Path):
        f = tmp_path / "empty.txt"
        f.write_text("", encoding="utf-8")
        assert handler({"path": str(f)}) == ""

    def test_multiline_content_preserved(self, tmp_path: Path):
        content = "line1\nline2\nline3"
        f = tmp_path / "multi.txt"
        f.write_text(content, encoding="utf-8")
        assert handler({"path": str(f)}) == content

    def test_returns_string(self, tmp_path: Path):
        f = tmp_path / "t.txt"
        f.write_text("x", encoding="utf-8")
        assert isinstance(handler({"path": str(f)}), str)
