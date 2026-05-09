"""Unit tests for the post-write formatter runner."""

from pathlib import Path
from unittest.mock import MagicMock, patch


from agent_on_claude_sdk.validation import format_if_python


class TestFormatIfPython:
    def test_returns_false_for_non_python(self, tmp_path: Path):
        f = tmp_path / "report.md"
        f.write_text("# hi")
        assert format_if_python(str(f)) is False

    def test_returns_true_for_python_file(self, tmp_path: Path):
        f = tmp_path / "script.py"
        f.write_text("x=1")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = format_if_python(str(f))
        assert result is True

    def test_calls_ruff_format_on_py_file(self, tmp_path: Path):
        f = tmp_path / "code.py"
        f.write_text("x=1")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            format_if_python(str(f))
        args = mock_run.call_args[0][0]
        assert args[0] == "ruff"
        assert args[1] == "format"
        assert str(f) in args

    def test_accepts_path_object(self, tmp_path: Path):
        f = tmp_path / "x.py"
        f.write_text("y=2")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = format_if_python(f)
        assert result is True

    def test_missing_ruff_does_not_raise(self, tmp_path: Path):
        f = tmp_path / "z.py"
        f.write_text("a=1")
        with patch("subprocess.run", side_effect=FileNotFoundError):
            result = format_if_python(f)  # must not raise
        assert result is True

    def test_txt_extension_skipped(self, tmp_path: Path):
        f = tmp_path / "notes.txt"
        f.write_text("hello")
        with patch("subprocess.run") as mock_run:
            format_if_python(f)
        mock_run.assert_not_called()
