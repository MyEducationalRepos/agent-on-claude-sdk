"""Tests for the related-links helper."""

from __future__ import annotations

from pathlib import Path

import pytest

from agent_on_claude_sdk.helpers.related_links import RelatedLinks, collect_local_paths


class TestRelatedLinksMarkdown:
    def test_has_local_paths_header(self):
        md = RelatedLinks().to_markdown()
        assert "## Local Paths" in md

    def test_has_external_links_header(self):
        md = RelatedLinks().to_markdown()
        assert "## External Links" in md

    def test_empty_local_shows_none(self):
        md = RelatedLinks().to_markdown()
        assert "*(none)*" in md

    def test_empty_external_shows_placeholder(self):
        md = RelatedLinks().to_markdown()
        assert "No external link available yet" in md

    def test_local_paths_rendered(self):
        rl = RelatedLinks(local_paths=["CLAUDE.md", "src/agent_on_claude_sdk/harness.py"])
        md = rl.to_markdown()
        assert "- CLAUDE.md" in md
        assert "- src/agent_on_claude_sdk/harness.py" in md

    def test_external_links_rendered(self):
        rl = RelatedLinks(external_links=["https://docs.anthropic.com"])
        md = rl.to_markdown()
        assert "- https://docs.anthropic.com" in md

    def test_both_sections_populated(self):
        rl = RelatedLinks(
            local_paths=["README.md"],
            external_links=["https://example.com"],
        )
        md = rl.to_markdown()
        assert "- README.md" in md
        assert "- https://example.com" in md
        assert "*(none)*" not in md
        assert "No external link available yet" not in md


class TestCollectLocalPaths:
    def test_returns_list(self, tmp_path: Path):
        result = collect_local_paths(tmp_path)
        assert isinstance(result, list)

    def test_finds_matching_files(self, tmp_path: Path):
        (tmp_path / "README.md").write_text("hello")
        result = collect_local_paths(tmp_path, patterns=["README.md"])
        assert "README.md" in result

    def test_sorted_output(self, tmp_path: Path):
        for name in ["z.md", "a.md", "m.md"]:
            (tmp_path / name).write_text("")
        result = collect_local_paths(tmp_path, patterns=["*.md"])
        assert result == sorted(result)

    def test_returns_posix_paths(self, tmp_path: Path):
        sub = tmp_path / "src"
        sub.mkdir()
        (sub / "foo.py").write_text("")
        result = collect_local_paths(tmp_path, patterns=["src/**/*.py"])
        assert all("/" in p or p.count("\\") == 0 for p in result)

    def test_empty_root_returns_empty(self, tmp_path: Path):
        result = collect_local_paths(tmp_path, patterns=["**/*.md"])
        assert result == []
