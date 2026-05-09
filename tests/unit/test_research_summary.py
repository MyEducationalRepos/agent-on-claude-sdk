"""Tests for the research-summary helper formatter."""

from __future__ import annotations


from agent_on_claude_sdk.helpers.research_summary import ResearchSummary


def _minimal() -> ResearchSummary:
    return ResearchSummary(
        question="What is the harness?",
        key_findings=["It wraps the SDK.", "It traces tool calls."],
    )


class TestSectionHeaders:
    def test_has_five_sections(self):
        md = _minimal().to_markdown()
        for i in range(1, 6):
            assert f"## {i}." in md

    def test_question_section_present(self):
        md = _minimal().to_markdown()
        assert "## 1. Question" in md
        assert "What is the harness?" in md

    def test_key_findings_listed(self):
        md = _minimal().to_markdown()
        assert "## 2. Key Findings" in md
        assert "- It wraps the SDK." in md
        assert "- It traces tool calls." in md

    def test_related_links_local_and_external_headers(self):
        md = _minimal().to_markdown()
        assert "**Local Paths**" in md
        assert "**External Links**" in md

    def test_next_step_section(self):
        md = ResearchSummary(
            question="Q", key_findings=["f"], next_step="Run the harness."
        ).to_markdown()
        assert "## 5. Next Step" in md
        assert "Run the harness." in md


class TestEmptyOptionals:
    def test_empty_local_paths_shows_none(self):
        md = _minimal().to_markdown()
        assert "*(none)*" in md

    def test_empty_evidence_gaps_shows_none(self):
        md = _minimal().to_markdown()
        assert "*(none identified)*" in md

    def test_empty_next_step_shows_placeholder(self):
        md = _minimal().to_markdown()
        assert "*(not specified)*" in md


class TestPopulatedOptionals:
    def test_local_paths_rendered(self):
        s = ResearchSummary(
            question="Q",
            key_findings=["f"],
            local_paths=["src/agent_on_claude_sdk/harness.py"],
        )
        md = s.to_markdown()
        assert "- src/agent_on_claude_sdk/harness.py" in md

    def test_external_links_rendered(self):
        s = ResearchSummary(
            question="Q",
            key_findings=["f"],
            external_links=["https://docs.anthropic.com"],
        )
        md = s.to_markdown()
        assert "- https://docs.anthropic.com" in md

    def test_evidence_gaps_rendered(self):
        s = ResearchSummary(
            question="Q",
            key_findings=["f"],
            evidence_gaps=["No benchmark data available."],
        )
        md = s.to_markdown()
        assert "- No benchmark data available." in md

    def test_multiple_findings(self):
        s = ResearchSummary(question="Q", key_findings=["A", "B", "C", "D", "E"])
        md = s.to_markdown()
        for letter in "ABCDE":
            assert f"- {letter}" in md
